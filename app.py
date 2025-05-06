from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import csv
import sys
import re
import os
import logging
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import (PyPDFLoader,TextLoader,UnstructuredWordDocumentLoader)
import main  # This is your main.py containing PDF processing logic
from langdetect import detect

# For Windows to fix stdout buffering
if os.name == 'nt':
    sys.stdout = open(sys.__stdout__.fileno(), mode='w', encoding='utf-8', buffering=1)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__,
            template_folder='frontend1/templates',
            static_folder='frontend1/static')

app.secret_key = 'your_secret_key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_FILE = os.path.join(BASE_DIR, 'user_inform.csv')
INPUT_DATA_FILE = os.path.join(BASE_DIR, 'user_input.csv')
CONTACT_DATA_FILE = os.path.join(BASE_DIR, 'contact_message.csv')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def initialize_csv():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'password'])

    if not os.path.exists(INPUT_DATA_FILE):
        with open(INPUT_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'question', 'difficulty', 'num_questions'])
    
    if not os.path.exists(CONTACT_DATA_FILE):
        with open(CONTACT_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'message'])


def is_user_registered(email):
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return any(row['email'] == email for row in reader)


def validate_login(email, password):
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email and row['password'] == password:
                return row['name']
    return None


@app.route('/')
def index():
    return redirect(url_for('quiz'))




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    initialize_csv()
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        logging.info("Signup received")

        if is_user_registered(email):
            flash('User already exists. Please log in.', 'error')
            return redirect(url_for('signup'))

        with open(USER_DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, password])

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    initialize_csv()
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('login'))

        name = validate_login(email, password)

        if name:
            session['user'] = name
            flash('Login successful!', 'success')
            return redirect(url_for('ai'))

        flash('Invalid email or password.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/quiz')
def quiz():
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    return render_template('quiz.html')


@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not all([name, email, message]):
        return jsonify({'status': 'fail', 'message': 'Missing required fields'}), 400

    with open(CONTACT_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, message])

    flash('✅ Thank you for contacting us! We will get back to you shortly.')
    return redirect(url_for('contact'))

    

    # # Prepare file path
    # csv_file = 'contact_messages.csv'
    # file_exists = os.path.isfile(csv_file)

    # # Write to CSV
    # with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     if not file_exists:
    #         writer.writerow(['Name', 'Email', 'Message'])  # header
    #     writer.writerow([name, email, message])


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/submit', methods=['POST'])
def submit():
    initialize_csv()
    data = request.json
    name = data.get('name')
    email = data.get('email')
    question = data.get('question')
    difficulty = data.get('difficulty')
    num_questions = data.get('num_questions')

    if not all([name, email, question, difficulty, num_questions]):
        return jsonify({'status': 'fail', 'message': 'Missing required fields'}), 400

    with open(INPUT_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, question, difficulty, num_questions])

    return jsonify({'status': 'success', 'message': 'Data stored successfully'}), 200


# ✅ This handles the PDF, .docx, .txt upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_file', methods=['POST'])
def upload_file():
    print("Upload endpoint hit")

    if 'file' not in request.files:
        print("No file part")
        return jsonify({'status': 'fail', 'message': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        print("No selected file")
        return jsonify({'status': 'fail', 'message': 'No selected file'}), 400
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.pdf', '.txt', '.docx']:
        return jsonify({'status': 'fail', 'message': 'Unsupported file format'}), 400

    if file: 
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved to: {file_path}")

        try:
            documents = main.load_full_document(file_path)
            if not documents:
                print("⚠️ Empty or unreadable PDF")
                return jsonify({'status': 'fail', 'message': 'The PDF file appears to be empty or unreadable.'}), 400
            else:
                # Extract and combine text for preview
                extracted_text = "\n".join(doc.page_content for doc in documents)
                lang = detect(extracted_text)
                if lang != 'en':
                    return jsonify({'status': 'fail', 'message': 'Only English PDFs are allowed.'}), 400
                print("PDF processing successful")
                return jsonify({
                    'status': 'success',
                    'message': f"PDF uploaded and processed.",
                    'filename': filename,
                    'content': extracted_text[:5000]
                }), 200

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return jsonify({'status': 'fail', 'message': str(e)}), 500

    return jsonify({'status': 'fail', 'message': 'Invalid file format'}), 400

@app.route('/generate_mcqs', methods=['POST'])
def generate_mcqs():
    from model import main  # Lazy import
    data = request.get_json()

    pdf_filename = data.get("filename")
    difficulty = data.get("difficulty")
    num_questions = int(data.get("num_questions"))

    if not pdf_filename:
        return jsonify({'status': 'fail', 'message': 'Missing filename'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

    try:
        full_docs = main.load_full_document(file_path)
        mcqs = main.generate_mcq(n_question=num_questions, difficulty=difficulty, n_option=4, documents=full_docs)
        json_generator = main.generate_json_from_mcqs(mcqs,output_path="output.json")

        return jsonify({'status': 'success', 'mcqs': json_generator}), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    from model import main  
    data = request.get_json()
    question = data.get('question')
    filename = data.get('filename')

    if not question or not filename:
        return jsonify({'status': 'fail', 'message': 'Missing question or filename'}), 400

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        db = main.create_vector_store(file_path)
        related_docs = main.retrieve_docs(db, question, k=4)
        response = main.question_pdf(question, related_docs)
        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

        return jsonify({'status': 'success', 'response': response})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)