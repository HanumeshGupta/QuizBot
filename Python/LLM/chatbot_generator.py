import main
import warnings
warnings.filterwarnings("ignore")


pdf_path = r"D:\Code\QuizBot\data\STA.pdf"

db = main.create_vector_store(pdf_path)

question = input("Enter the Question : ")

related_doc = main.retrieve_docs(db,question,k=4)

generator = main.question_pdf(question,related_doc)
print(generator)
