# Backend Setup Guide - AI Examination System

## Complete Installation & Configuration Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **pip** (Python package manager)
3. **Git** (optional, for version control)

---

## Step 1: Project Structure

Your project should now have this structure:

```
AI-Based-Automated-Examination/
│
├── index.html                      # Frontend HTML file
├── README.md
├── PROJECT_INTRODUCTION.md
│
└── backend/
    ├── app.py                      # Main Flask application
    ├── models.py                   # Database models
    ├── ai_generator.py             # AI question generator
    ├── config.py                   # Configuration settings
    └── requirements.txt            # Python dependencies
```

---

## Step 2: Install Python Dependencies

### For Windows (PowerShell):

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

### For Linux/Mac:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step 3: Database Setup

The database will be created automatically when you first run the application.

### SQLite (Default - No setup needed)
- Database file: `exam_system.db` (created automatically)
- Perfect for development and testing

### MySQL (Optional - Production)

If you want to use MySQL instead:

1. Install MySQL Server
2. Create database:
   ```sql
   CREATE DATABASE exam_system;
   ```

3. Update `app.py` line 9:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/exam_system'
   ```

4. Install MySQL connector:
   ```bash
   pip install pymysql
   ```

### PostgreSQL (Optional - Production)

For PostgreSQL:

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE exam_system;
   ```

3. Update `app.py` line 9:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/exam_system'
   ```

4. Install PostgreSQL connector:
   ```bash
   pip install psycopg2
   ```

---

## Step 4: Run the Backend Server

```powershell
# Make sure you're in the backend folder with venv activated
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Database tables created!
```

**Keep this terminal running!**

---

## Step 5: Run the Frontend

### Option 1: Using VS Code Live Server (Recommended)

1. Open `index.html` in VS Code
2. Right-click and select "Open with Live Server"
3. Your browser will open at `http://127.0.0.1:5500`

### Option 2: Using Python HTTP Server

In a NEW terminal (keep backend running):

```powershell
# From project root folder
cd d:\AI-Based-Automated-Examination
python -m http.server 8000
```

Open browser: `http://localhost:8000`

### Option 3: Direct File Open

Simply double-click `index.html` (but CORS might not work properly)

---

## Step 6: Test the Application

1. **Open frontend** in browser
2. **Click "Get Started"** → Register a new user
3. **Fill registration form**:
   - Name: Test User
   - Email: test@example.com
   - Password: password123

4. **Login** with your credentials
5. **Configure exam**:
   - Select Subject (e.g., Artificial Intelligence)
   - Choose Total Marks (25, 35, or 50)
   - Select Difficulty (Beginner, Intermediate, Pro)

6. **Click "Start AI-Powered Examination"**
7. **Answer questions** and submit
8. **View results** with detailed analysis

---

## Database Tables Created

The system automatically creates these tables:

### 1. **users**
- Stores user registration data
- Fields: id, name, email, password_hash, created_at

### 2. **subjects**
- Contains exam subjects
- Fields: id, name, description, created_at

### 3. **questions**
- Stores all generated questions
- Fields: id, subject_id, question_text, question_type, options, correct_answer, explanation, marks, difficulty, topic

### 4. **exams**
- Tracks each exam session
- Fields: id, user_id, subject_id, total_marks, difficulty, start_time, end_time

### 5. **exam_answers**
- Stores user answers for each question
- Fields: id, exam_id, question_id, user_answer, is_correct, marks_awarded

### 6. **exam_results**
- Final exam results
- Fields: id, exam_id, total_marks, max_marks, correct_answers, wrong_answers, negative_marks, percentage

---

## API Endpoints Reference

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login

### Exam Management
- `POST /api/generate-questions` - Generate exam questions
- `POST /api/submit-exam` - Submit and evaluate exam
- `GET /api/exam-history/<user_email>` - Get user's exam history

---

## Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port 5000 already in use"
Change port in `app.py` (last line):
```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

And update frontend `index.html` (line 167):
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

### Error: "CORS policy blocked"
Make sure:
1. Backend is running on `http://localhost:5000`
2. `flask-cors` is installed
3. CORS is enabled in `app.py`

### Error: "Cannot connect to backend"
1. Check backend is running (terminal should show Flask server)
2. Check `API_BASE_URL` in `index.html` matches backend URL
3. Try accessing http://localhost:5000/api/test in browser

### Database not creating
1. Delete any existing `.db` files
2. Restart backend server
3. Check file permissions in backend folder

---

## Advanced: AI Integration with OpenAI

To use real AI for question generation:

### 1. Install OpenAI package:
```bash
pip install openai
```

### 2. Get API key from OpenAI:
- Visit https://platform.openai.com/
- Create account / Login
- Go to API Keys section
- Create new key

### 3. Set environment variable:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 4. Update `ai_generator.py`:

Uncomment the OpenAI integration code at the bottom of the file and replace the template functions.

---

## Production Deployment

### 1. Update Secret Key
In `app.py`, change:
```python
app.config['SECRET_KEY'] = 'your-very-secure-random-secret-key'
```

### 2. Disable Debug Mode
```python
app.run(debug=False)
```

### 3. Use Production Database
Switch from SQLite to MySQL/PostgreSQL

### 4. Deploy Options:
- **Heroku**: Easy deployment with PostgreSQL
- **AWS EC2**: Full control
- **DigitalOcean**: Simple VPS hosting
- **PythonAnywhere**: Python-specific hosting

---

## Environment Variables (.env file)

Create `.env` file in backend folder:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///exam_system.db
OPENAI_API_KEY=your-openai-key
FLASK_ENV=development
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Update `app.py` to load env:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Testing the API with Postman/curl

### Register User:
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"pass123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}'
```

### Generate Questions:
```bash
curl -X POST http://localhost:5000/api/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "subject":"Artificial Intelligence",
    "total_marks":25,
    "difficulty":"Beginner",
    "user_id":"test@test.com"
  }'
```

---

## Next Steps

1. ✅ Backend API is ready
2. ✅ Database configured
3. ✅ Frontend connected
4. 🔄 Add more questions to `ai_generator.py`
5. 🔄 Integrate real AI (OpenAI/Hugging Face)
6. 🔄 Add user authentication with JWT
7. 🔄 Create admin panel for question management
8. 🔄 Deploy to production

---

## Support & Documentation

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **OpenAI API**: https://platform.openai.com/docs/

---

**Created for: Intelligent Chatbot for Automated Examination Project**  
**Backend: Python Flask + SQLAlchemy**  
**Frontend: HTML5 + JavaScript**  
**Database: SQLite (Development) / MySQL/PostgreSQL (Production)**
