# 🤖 Intelligent Chatbot for Automated Examination

## 📌 Project Definition

**Intelligent Chatbot for Automated Examination** is an AI-powered conversational system that automatically generates exam questions, conducts examinations through a chat interface, evaluates user answers using Natural Language Processing (NLP), justifies the evaluation, and analyzes learner weaknesses to provide personalized feedback and improvement suggestions.

The system aims to simulate a human-like examiner that not only checks answers but also explains mistakes and guides learners toward better understanding.

## 🎯 Objectives

- Automate question generation and examination process
- Evaluate descriptive answers using NLP techniques
- Provide justification for marks (right/wrong/partial)
- Identify topic-wise weaknesses of learners
- Offer personalized learning suggestions

## 🧠 Core Properties

- **Intelligent**: Uses NLP and semantic analysis instead of simple keyword matching
- **Adaptive**: Feedback and suggestions change based on user performance
- **Interactive**: Exam is conducted in a conversational (chat-based) manner
- **Explainable AI**: Justifies every evaluation decision
- **Student-Centric**: Focuses on learning improvement, not just scoring

## ✨ Key Features

- 📚 Automatic Question Generation (MCQ & Descriptive)
- 💬 Chat-Based Examination System
- 🧠 NLP-Based Answer Evaluation
- 📝 Answer Justification & Explanation
- 📊 Weakness Detection & Performance Analysis
- 🎯 Personalized Improvement Suggestions
- 🗂️ Exam History & Result Tracking

## 🛠️ Technology Stack

### 🔹 Backend
- Python
- Flask / FastAPI

### 🔹 AI & NLP
- OpenAI API / HuggingFace Inference API
- spaCy / NLTK
- Sentence Transformers (Semantic Similarity)

### 🔹 Database
- SQLite / MySQL

### 🔹 Frontend
- HTML5 + TailwindCSS
- Vanilla JavaScript (ES6+)
- Responsive Design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser
- Code editor (VS Code recommended)

### Installation

**1. Clone/Download the project**

```bash
cd AI-Based-Automated-Examination
```

**2. Setup Backend**

```powershell
# Windows
cd backend
.\start.bat

# Linux/Mac
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Backend runs on: `http://localhost:5000`


run the project using : 'cd D:\AI-Based-Automated-Examination\backend
.\venv\Scripts\python.exe app.py '

**3. Run Frontend**

Option A: Using Live Server (VS Code)
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

Option B: Using Python
```bash
python -m http.server 8000
```
Open: `http://localhost:8000`

**4. Start Testing**
- Register a new account
- Select subject, marks, and difficulty
- Start AI-powered examination
- View detailed results

## 📁 Project Structure

```
AI-Based-Automated-Examination/
│
├── index.html                    # Main frontend application
├── README.md                     # Project documentation
├── PROJECT_INTRODUCTION.md       # Academic introduction
├── BACKEND_SETUP_GUIDE.md       # Detailed backend setup
│
└── backend/
    ├── app.py                   # Flask API server
    ├── models.py                # Database models
    ├── ai_generator.py          # AI question generator
    ├── config.py                # Configuration
    ├── init_db.py              # Database initialization
    ├── requirements.txt         # Python dependencies
    ├── start.bat               # Windows startup script
    └── README.md               # Backend documentation
```

## 🔧 System Features

### Implemented ✅
- User registration and authentication
- Subject selection (AI, Networks, Graphics, Compiler)
- Difficulty levels (Beginner, Intermediate, Pro)
- Multiple question types (MCQ, True/False, Viva)
- AI-powered question generation
- Automated answer evaluation
- NLP-based Viva answer analysis
- Negative marking system (-0.25 for MCQ)
- Real-time exam timer with auto-submit
- Detailed result analysis
- Exam history tracking

### Database Schema
- **Users**: Secure user management
- **Subjects**: Exam subject catalog
- **Questions**: Dynamic question bank
- **Exams**: Exam session tracking
- **Exam Answers**: User responses
- **Exam Results**: Performance analytics

## 🧩 NLP Techniques Used

- Tokenization
- Lemmatization
- Keyword Extraction
- Semantic Similarity Analysis
- Text Classification
- Context Management

## 🔌 API Documentation

### Authentication Endpoints

**Register User**
```
POST /api/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure123"
}
```

**User Login**
```
POST /api/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure123"
}
```

### Exam Endpoints

**Generate Questions**
```
POST /api/generate-questions
Content-Type: application/json

{
  "subject": "Artificial Intelligence",
  "total_marks": 25,
  "difficulty": "Intermediate",
  "user_id": "john@example.com"
}
```

**Submit Exam**
```
POST /api/submit-exam
Content-Type: application/json

{
  "user_id": "john@example.com",
  "answers": [
    {"question_id": 1, "answer": "A"},
    {"question_id": 2, "answer": "True"},
    {"question_id": 3, "answer": "Detailed text answer..."}
  ]
}
```

**Get Exam History**
```
GET /api/exam-history/<user_email>
```

## 📈 Expected Outcome

- Fair and explainable automated exam evaluation
- Improved learning through personalized feedback
- Reduction of manual exam checking workload
- Better understanding of student weaknesses

## 🚀 Future Goals

- 🔊 Voice-based examination system
- 🌐 Multilingual support
- 📱 Mobile application integration
- 📈 Adaptive difficulty based on performance
- 🧪 Cheating detection using behavior analysis
- 📚 Integration with Learning Management Systems (LMS)

## 🎓 Academic Relevance

This project demonstrates practical implementation of:

- Artificial Intelligence
- Natural Language Processing
- Conversational Systems
- Automated Assessment
- Personalized Learning Systems
