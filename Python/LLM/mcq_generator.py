import main
import warnings
warnings.filterwarnings("ignore")


pdf_path = r"D:\Code\QuizBot\data\STA.pdf"

full_docs = main.load_full_document(pdf_path)

mcqs = main.generate_mcq(n_question=10, difficulty="easy", n_option=4, documents=full_docs)
print(mcqs)
