from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

os.environ["OLLAMA_MODELS_PATH"] = r"Z:\OLLAMA\models"  # Path of Ollama

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b") # Name of Ollama model using 
model = OllamaLLM(model="deepseek-r1:1.5b")
# Load documents from a specified directory
data = r"QuizBot\data\SOP.pdf"
template = """Given the question, provide a detailed context that includes relevant background information, key concepts, and any necessary definitions to help understand the question fully.
Question : {question}
Context : {context}
"""


# This define the Input PDF Vectors
def create_vector_store(data):
   loader = PyPDFLoader(data)
   documents = loader.load()

   text_splitter = RecursiveCharacterTextSplitter(
       chunk_size = 2000,
       chunk_overlap =300,
       add_start_index=True
   )

   chunked_docs = text_splitter.split_documents(documents)
   db = FAISS.from_documents(chunked_docs,embeddings)
   return db

# This search for Similarity in data [For Chat Bot]
def retrieve_docs(db,query,k=4):
    return db.similarity_search(query,k)

# This generate Output
def question_pdf(question,documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    return chain.invoke({"question": question, "context" : context})





# # Check if documents were loaded successfully
# if documents:
#     print(documents[0])  # Access the first document
# else:
#     print("No documents found in the specified directory.")



### This is for MCQ generator  

def generate_mcq (n_question,difficulty,n_option, documents) :
    
    template = (
        "You are an AI model designed to generate multiple-choice questions (MCQs). "
        "Your task is to create {n_question} MCQs based on the content of the provided PDF. "
        "Each question should match the {difficulty} difficulty level. For each question, provide "
        "{n_option} answer choices, with only one correct answer. At the end of each question, include "
        "the correct answer labeled clearly.\n\n"
        "Content:\n{context}"
    )

    prompt = ChatPromptTemplate.from_template(template)
    context = "\n\n".join([doc.page_content for doc in documents])

    chain = prompt | model

    result = chain.invoke({
        "n_question": n_question,
        "difficulty": difficulty,
        "n_option": n_option,
        "context": context
    })

    return result

