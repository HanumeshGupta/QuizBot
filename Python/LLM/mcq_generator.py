import main
import extract_info
import warnings
import re
warnings.filterwarnings("ignore")

pdf_path = r"Z:\QuizBot\data\00009.pdf"

# full_docs = main.load_full_document(pdf_path)

# mcqs = main.generate_mcq(n_question=10, difficulty="hard", n_option=4, documents=full_docs)
# print(mcqs)
# data= main.patten_clear(mcqs)
# print(data)
# # Print the structured array (for testing purposes)

full_docs = main.load_full_document(pdf_path)

# Generate MCQs
mcqs = main.generate_mcq(n_question=10, difficulty="easy", n_option=4, documents=full_docs)

print(mcqs)

# info = extract_info.extract_info(mcqs)

# print (info)
