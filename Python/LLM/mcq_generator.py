# import main
# import extract_info
# import warnings
# import re
# warnings.filterwarnings("ignore")

# pdf_path = r"Z:\QuizBot\data\00009.pdf"

# # full_docs = main.load_full_document(pdf_path)

# # mcqs = main.generate_mcq(n_question=10, difficulty="hard", n_option=4, documents=full_docs)
# # print(mcqs)
# # data= main.patten_clear(mcqs)
# # print(data)
# # # Print the structured array (for testing purposes)

# full_docs = main.load_full_document(pdf_path)

# # Generate MCQs
# mcqs = main.generate_mcq(n_question=10, difficulty="easy", n_option=4, documents=full_docs)

# print(mcqs)

# # info = extract_info.extract_info(mcqs)

# # print (info)


# Created Seperate MCQ_Generator Code.

import re
import json
import warnings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
import datetime

warnings.filterwarnings("ignore")


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
def generate_json_from_mcqs(mcq_text):
    prompt = prompt = f"""
    You will be given a list of multiple choice questions (MCQs) with options. Your task is to convert them into JSON format.

    🟢 Instructions:
    1. Extract the question text and the actual option texts (not placeholders like "Option A").
    2. Ensure the options are stored as a list of strings, in the order they appear (A, B, C, D).
    3. Extract the correct answer text (NOT just the letter like "A" or "B", but the full text of the correct option).
    4. Format the final output as a JSON list of objects with this structure:

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

    # Use Ollama LLM to generate JSON-formatted MCQs
    response = model.invoke(prompt)  # model.chat() only if you're bypassing LangChain

    if isinstance(response, dict):
        response_text = response.get("text", "")
    else:
        response_text = response

    


    # Remove markdown-style code fences and artifacts
    cleaned_text = re.sub(r"```(?:json)?", "", response_text, flags=re.IGNORECASE).strip()
    cleaned_text = re.sub(r"<think>.*?</think>", "", cleaned_text, flags=re.DOTALL | re.IGNORECASE)
    print("🔍 Raw LLM response:")
    print(response_text)

    try:
        json_data = json.dumps(response_text)
        return json_data
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        return None
    

if __name__ == "__main__":
    pdf_path = r"D:\Code\QuizBot\data\00009.pdf"  # Replace with your actual path

    print("📄 Loading and processing PDF...")
    full_docs = load_full_document(pdf_path)

    print("🧠 Generating MCQs...")
    mcqs = generate_mcq(n_question=10, difficulty="easy", n_option=4, documents=full_docs)

    if mcqs:
        print("\n🎉 MCQs successfully generated and saved!\n")

    print(mcqs)

    question = generate_json_from_mcqs(mcqs)

    print(question)





