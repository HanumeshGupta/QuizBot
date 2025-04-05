import streamlit as st
import main as main

st.title("Chat with PDFs with Deepseek")
data = r"QuizBot\data\SOP.pdf"
# uploaded_file = st.file_uploader(
#     "Upload PDF",
#     type = "pdf",
#     accept_multiple_files = False
# )

db = main.create_vector_store(data)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input box
question = st.chat_input("Ask something about the PDF...")

if question:
    # Add user question to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.write(question)

    # Retrieve relevant documents
    related_documents = main.retrieve_docs(db, question, k=4)

    # Generate answer
    answer = main.question_pdf(question, related_documents)

    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)

