from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import csv
import sys
import os

if os.name == 'nt':  # Windows fix
    sys.stdout = open(sys.__stdout__.fileno(), mode='w', encoding='utf-8', buffering=1)

import logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__,
            template_folder='frontend1/templates',  
            static_folder='frontend1/static')                


app.secret_key = 'your_secret_key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_FILE = os.path.join(BASE_DIR, 'user_inform.csv')
INPUT_DATA_FILE = os.path.join(BASE_DIR, 'user_input.csv')


# Ensure both CSV files exist
def initialize_csv():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'password'])

    if not os.path.exists(INPUT_DATA_FILE):
        with open(INPUT_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'question', 'difficulty', 'num_questions'])

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
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    initialize_csv()
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        #print(f"Received signup: {name}, {email}, {password}")
        #print("Signup received")
        # print("Signup received")
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
        password = request.form['password']
        name = validate_login(email, password)

        if name:
            session['user'] = name
            flash('Login successful!', 'success')
            return redirect(url_for('ai'))

        flash('Invalid email or password.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/ai')
def ai():
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    return f"Welcome {session['user']}! You're now logged in."

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

if __name__ == '__main__':
    app.run(debug=True)
