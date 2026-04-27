# 🎯 QUICK START GUIDE

## What Was Changed

### ✅ Frontend (index.html)
- ❌ **Removed**: Mock/default question generation
- ✅ **Added**: API integration for real backend communication
- ✅ **Updated**: Subjects to match your requirements (AI, Networks, Graphics, Compiler)
- ✅ **Added**: Difficulty level selector (Beginner, Intermediate, Pro)
- ✅ **Updated**: Total marks options (25, 35, 50)
- ✅ **Added**: Dynamic question rendering (MCQ, True/False, Viva)

### ✅ Backend Created (Python Flask)
- ✅ `app.py` - Main Flask API server with all endpoints
- ✅ `models.py` - Database models (6 tables)
- ✅ `ai_generator.py` - AI question generator with question bank
- ✅ `config.py` - Configuration management
- ✅ `requirements.txt` - All Python dependencies
- ✅ `init_db.py` - Database initialization script
- ✅ `start.bat` - Easy Windows startup

### ✅ Documentation
- ✅ `BACKEND_SETUP_GUIDE.md` - Complete setup instructions
- ✅ `README.md` - Unified full project and backend API documentation

---

## 🚀 How to Run Your Project

### Step 1: Start the Backend

Open PowerShell in your project folder:

```powershell
cd backend
.\start.bat
```

**What happens:**
- Creates virtual environment (if needed)
- Installs all dependencies
- Creates database automatically
- Starts server on http://localhost:5000

**Keep this terminal open!**

### Step 2: Open Frontend

**Option A: VS Code Live Server (Easiest)**
1. Open `index.html` in VS Code
2. Right-click → "Open with Live Server"
3. Browser opens automatically

**Option B: Python HTTP Server**
```powershell
# In a NEW PowerShell terminal
cd d:\AI-Based-Automated-Examination
python -m http.server 8000
```
Then open: http://localhost:8000

### Step 3: Test the Application

1. **Register**: Click "Get Started" → Create account
2. **Login**: Sign in with your credentials
3. **Configure Exam**:
   - Subject: Artificial Intelligence
   - Total Marks: 25
   - Difficulty: Beginner
4. **Start Exam**: Answer questions
5. **Submit**: View detailed results

---

## 📊 Database Structure

Your system automatically creates these tables:

| Table | Purpose |
|-------|---------|
| `users` | User accounts (name, email, password) |
| `subjects` | Exam subjects (AI, Networks, etc.) |
| `questions` | Generated questions with answers |
| `exams` | Exam sessions with timestamps |
| `exam_answers` | User answers for each question |
| `exam_results` | Final results with analytics |

**Database File**: `backend/exam_system.db` (SQLite)

To reset database:
```powershell
cd backend
python init_db.py
```

---

## 🔧 How to Add More Questions

Edit `backend/ai_generator.py`:

```python
'Artificial Intelligence': {
    'Beginner': {
        'MCQ': [
            {
                'question': 'Your question here?',
                'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                'correct_answer': 'A',
                'explanation': 'Why this is correct',
                'topic': 'Topic name'
            },
            # Add more questions...
        ]
    }
}
```

Restart the backend after adding questions.

---

## 💡 How the System Works

### Question Generation Flow:
1. User selects subject + marks + difficulty
2. Frontend calls → `POST /api/generate-questions`
3. Backend creates exam session in database
4. AI generator picks questions from bank
5. Questions sent to frontend
6. Timer starts

### Answer Evaluation Flow:
1. User submits answers
2. Frontend calls → `POST /api/submit-exam`
3. Backend evaluates each answer:
   - **MCQ/True-False**: Exact match checking
   - **Viva**: NLP similarity analysis
4. Calculates:
   - Total marks
   - Correct/wrong count
   - Negative marks (MCQ only: -0.25)
   - Percentage
5. Saves result to database
6. Returns detailed analysis

---

## 🔌 API Endpoints Available

### User Management
- `POST /api/register` - Create account
- `POST /api/login` - User login

### Exam System
- `POST /api/generate-questions` - Generate exam
- `POST /api/submit-exam` - Submit & evaluate
- `GET /api/exam-history/<email>` - View history

Test in browser: http://localhost:5000/api/test

---

## 🎨 Customize Frontend

In `index.html`, you can change:

**API URL** (if backend port changes):
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

**Colors**: Search for `bg-blue-600` and replace with your color

**Timer**: Line ~300, change formula:
```javascript
startTimer(totalMarks * 1.5); // 1.5 minutes per mark
```

---

## 🧠 Add Real AI (OpenAI)

### 1. Install OpenAI
```powershell
cd backend
pip install openai
```

### 2. Get API Key
- Go to: https://platform.openai.com/
- Create account
- Get API key from dashboard

### 3. Set Environment Variable
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

### 4. Update `ai_generator.py`
Use the OpenAI integration code at the bottom of the file.

---

## 🐛 Common Issues & Solutions

### "Module not found: flask"
```powershell
cd backend
pip install -r requirements.txt
```

### "Port 5000 already in use"
Edit `app.py` last line:
```python
app.run(debug=True, port=5001)
```

And `index.html` line ~167:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

### "Cannot connect to backend"
1. Check backend terminal - should show "Running on http://127.0.0.1:5000"
2. Check no firewall blocking
3. Try http://localhost:5000 in browser

### "Database locked"
Close all Python processes and restart backend

---

## 📚 File Reference

### Must Edit Files:
- `backend/ai_generator.py` → Add questions
- `backend/app.py` → Change secret key for production

### Configuration Files:
- `backend/config.py` → Database, debug settings
- `backend/requirements.txt` → Python packages

### Documentation:
- `BACKEND_SETUP_GUIDE.md` → Detailed setup
- `PROJECT_INTRODUCTION.md` → Academic write-up
- `README.md` → Full project info

---

## ✨ Next Steps

1. ✅ **Test the system** - Make sure everything works
2. 📝 **Add more questions** - Expand question bank
3. 🤖 **Integrate real AI** - OpenAI/Hugging Face
4. 🎨 **Customize UI** - Change colors/layout
5. 🔐 **Add JWT auth** - Secure API endpoints
6. 📊 **Add analytics** - Performance graphs
7. 🚀 **Deploy online** - Heroku/AWS/DigitalOcean

---

## 🆘 Need Help?

1. **Check logs**: Backend terminal shows all errors
2. **Read docs**: `BACKEND_SETUP_GUIDE.md` has detailed info
3. **Test API**: Use browser or Postman to test endpoints
4. **Database**: Use DB Browser for SQLite to view data

---

## 🎓 Project Structure Summary

```
Your Project/
│
├── index.html                    Frontend (UI)
├── QUICK_START.md               This guide
├── README.md                     Main documentation
├── BACKEND_SETUP_GUIDE.md       Detailed setup
│
└── backend/
    ├── start.bat                🚀 START HERE!
    ├── app.py                   API server
    ├── models.py                Database structure
    ├── ai_generator.py          Question bank
    └── exam_system.db           Database (auto-created)
```

---

**System Status**: ✅ Ready to Use  
**Backend**: Python Flask + SQLAlchemy  
**Frontend**: HTML5 + Tailwind + JavaScript  
**Database**: SQLite (Development)  

**To start testing**: Run `backend\start.bat` and open `index.html`

🎉 **Happy Coding!**
