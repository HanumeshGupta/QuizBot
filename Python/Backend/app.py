from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import csv
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "user_info.csv")
import pdfplumber
import docx
from werkzeug.utils import secure_filename
from fpdf import FPDF


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flashing messages

USER_FILE = "user_info.csv"

# Ensure the CSV exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "password"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    print(f"[REGISTER] Email: {email}, Password: {password}, Confirm: {confirm}")

    if not email or not password or not confirm:
        flash("Please fill all the fields.")
        return redirect(url_for("home"))

    if password != confirm:
        flash("Passwords do not match.")
        return redirect(url_for("home"))

    # Check if user exists
    with open(USER_FILE, mode="r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == email:
                flash("User already registered.")
                return redirect(url_for("home"))

    # Register the user
    with open(USER_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email, password])
        print(f"Registered {email} with password {password}")

    
    flash("Registration successful!")
    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    print(f"[LOGIN] Email: {email}, Password: {password}")

    with open(USER_FILE, mode="r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            
            if len(row) < 2:
                continue
            print(f"Checking row: {row}")
            if row[0] == email and row[1] == password:
                flash("Login successful!")
                return redirect(url_for("home"))

    flash("Invalid email or password.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
print("Current working directory:", os.getcwd())
