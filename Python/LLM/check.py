import main

pdf_path = r"D:\Code\QuizBot\data\STA.pdf"
db = main.create_vector_store(pdf_path)
docs = main.retrieve_docs(db, query="", k=5)

mcqs = main.generate_mcq(n_question=5, difficulty="medium", n_option=4, documents=db)
print(mcqs)