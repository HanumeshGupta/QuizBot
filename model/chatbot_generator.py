import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
import re

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

def retrieve_docs(docs, query, k=4):
    db = FAISS.from_documents(docs, embeddings)
    return db.similarity_search(query, k)

def question_pdf(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    
    template = """Given the question, provide a detailed context that includes relevant background information, key concepts, and any necessary definitions to help understand the question fully.
Question: {question}
Context: {context}
"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})

# Main Code

pdf_path = r"Z:\QuizBot\data\00009.pdf"

# Retriving the Pdf
full_docs = create_vector_store(pdf_path)

# Taking Input
question = input("Enter the Question: ")

# Retriving Similar data
related_docs = retrieve_docs(full_docs, question, k=4)

# Generating Text
generated_context = question_pdf(question, related_docs)

print("\nGenerated Context:\n")
result = re.sub(r"<think>.*?</think>", "", generated_context, flags=re.DOTALL).strip()
print(result)
