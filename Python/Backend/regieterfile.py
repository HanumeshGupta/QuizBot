import csv
import os
import flask
import pdfplumber
import docx
from werkzeug.utils import secure_filename
from fpdf import FPDF

def register():
    
    if not os.path.exists("user_info.csv"):
        with open("user_info.csv", mode="w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["email", "password"])

    
    email = input("Please enter your Email: ")
    
    
    with open("user_info.csv", mode="r") as f_read:
        reader = csv.reader(f_read, delimiter=",")
        for row in reader:
            if row[0] == email:
                print("Already registered!")
                return

    
    password = input("Please enter your Password: ")
    password2 = input("Please Re-type your Password: ")

    
    if password == password2:
        with open("user_info.csv", mode="a", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([email, password])  
        print("Registration successful!")
    else:
        print("Password does not match.")

def login():
    
    email = input("Please enter your Email: ")
    password = input("Please enter your Password: ")

    
    with open("user_info.csv", mode="r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)  
        for row in reader:
            if row[0] == email and row[1] == password:
                print("Logged in successfully!")
                return True
    print("Invalid email or password. Please try again!")
    return False


register()
login()
