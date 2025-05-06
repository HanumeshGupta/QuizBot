from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import os
import re



# ChatBot 

# Model is Embedding here.
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
model = OllamaLLM(model="deepseek-r1:1.5b")

# Functions are collected here : 

def create_vector_store(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)


def retrieve_docs(vector_store, query, k=4):
    vector_store = FAISS.from_documents(vector_store, embeddings)
    return vector_store.similarity_search(query, k)

def question_pdf(question,  related_docs):
    context = "\n\n".join([doc.page_content for doc in  related_docs])
    
    template = """Given the question, provide a detailed context that includes relevant background information, key concepts, and any necessary definitions to help understand the question fully.
Question: {question}
Context: {context}
"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})


## MCQ Generator 

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
model = OllamaLLM(model="deepseek-r1:1.5b")


def load_full_document(data_path):
    loader = PyPDFLoader(data_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def generate_mcq(n_question, difficulty, n_option, documents, output_file=None):
    template = (
        '''You are an AI model designed to generate multiple-choice questions (MCQs). 
        Your task is to create {n_question} MCQs based on the content of the provided PDF. 
        Each question should match the {difficulty} difficulty level. For each question, provide 
        {n_option} answer choices, with only one correct answer. At the end of each question, include 
        the correct answer labeled clearly.\n\n
        Content:\n{context}'''
    )

    prompt = ChatPromptTemplate.from_template(template)
    context = "\n\n".join([doc.page_content for doc in documents[:5]])

    chain = prompt | model
    result = chain.invoke({
        "n_question": n_question,
        "difficulty": difficulty,
        "n_option": n_option,
        "context": context
    })

    if isinstance(result, str):
        result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()

    return result

# On - Going Works [Converting MCQS text to json File.]
def generate_json_from_mcqs(mcq_text, output_path="output.json"):
    prompt = f"""
    You will be given a list of multiple choice questions (MCQs) with options. Your task is to convert them into JSON format.

    🟢 Instructions:
    1. Extract the question text and the actual option texts (not placeholders like "Option A").
    2. Ensure the options are stored as a list of strings, in the order they appear (A, B, C, D).
    3. Extract the correct answer text (NOT just the letter like "A" or "B", but the full text of the correct option).
    4. If the Correct answer is not given in the extract... then find the answer in that.
    5. Format the final output as a JSON list of objects with this structure:

    [
        {{
            "question": "Full question text here... it will end with '?' in the end.",
            "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
            "answer": "Correct Option Text"
        }},
        ...
    ]

    📝 MCQs:
    {mcq_text}

    Return only the final JSON. Do not include explanations or markdown.
    """

    response = model.invoke(prompt)

    if isinstance(response, dict):
        response_text = response.get("text", "")
    else:
        response_text = response

    cleaned_text = re.sub(r"```(?:json)?", "", response_text, flags=re.IGNORECASE).strip()
    cleaned_text = re.sub(r"<think>.*?</think>", "", cleaned_text, flags=re.DOTALL | re.IGNORECASE)

    try:
        json_data = json.loads(cleaned_text)  # Parse the actual JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print(f"✅ JSON file saved to {output_path}")
        return json_data
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        return None