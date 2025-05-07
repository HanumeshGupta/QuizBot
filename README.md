# 🤖 QuizBot – AI-Powered Question Generator

Transform your study sessions into interactive learning with **QuizBot**! This AI-driven app reads PDF or text content and generates Multiple Choice Questions (MCQs) with correct answers using the **Ollama LLM**. Built with a sleek Tailwind CSS frontend and a robust Python Flask backend, QuizBot is your personal intelligent quiz companion.

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Contributors](#-contributors)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 🌟 Overview

**QuizBot** helps students, teachers, and self-learners convert documents into interactive quizzes using AI. Just upload a file, and let QuizBot do the rest.

- Accepts PDF and text inputs.
- Generates structured MCQs with accurate answers.
- Uses Ollama-powered Language Models to understand and summarize content intelligently.

---

## 🛠️ Features

✅ Upload PDFs or enter raw text.  
✅ Extracts content using powerful LLMs.  
✅ Generates high-quality MCQs with answers.  
✅ Clean, mobile-friendly UI with Tailwind CSS.  
✅ Flask backend integrated with Ollama LLM for prompt processing.

---

## 🧰 Tech Stack

- **Frontend**: HTML, JS, Tailwind CSS  
- **Backend**: Flask (Python)  
- **AI/LLM**: [Ollama](https://ollama.com/)  
- **PDF Parsing**: `PyMuPDF` (`fitz`)  
- **LLM Integration**: Custom Lua + Python pipeline

---

## 🚀 Getting Started

### 🛠️ Prerequisites

- Python 3.8+
- Flask
- Ollama LLM (running locally or via API)
- PyMuPDF
- Tailwind (precompiled in static folder)

---

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/QuizBot.git
cd QuizBot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask development server
python app.py
```

---

## 🎯 Usage

- Visit http://localhost:5000 in your browser.

- Upload a PDF or paste your study notes.

- Click "Generate Quiz".

- Instantly view AI-generated MCQs with correct answers.

---

## 📂 Project Structure

``` 
QuizBot/
├── app.py              # Main Flask backend
├── main.py             # LLM processing and generation logic
├── templates/
│   └── index.html      # Tailwind-powered frontend
├── static/
│   └── style.css       # Tailwind CSS (optional overrides)
├── uploads/            # User-uploaded PDFs
├── requirements.txt    # Python dependencies
└── README.md           # This file!
```

---

## 🤝 Contributors

| Name    | Role                          | GitHub                                       |
| ------- | ----------------------------- | -------------------------------------------- |
| Harsh   | 🔌 Backend Connectivity       | [@harshdev](https://github.com/harshdev)     |
| You     | 🧠 LLM Integration & Pipeline | [@yourhandle](https://github.com/yourhandle) |
| Aditya  | 💻 Website Development        | [@adityadev](https://github.com/adityadev)   |
| Tanisha | 📋 Project Management         | [@tanishapm](https://github.com/tanishapm)   |

---

## 🔮 Future Enhancements

- User login & history tracking

- MCQ export (PDF/CSV)

- OCR/image-based PDF support

- Quiz scoring + gamification

- Deployment to Render/Heroku/AWS

---

## 📝 License
This project is licensed under the MIT License.

