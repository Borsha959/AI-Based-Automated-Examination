# AI Examination System - Backend API

Python Flask backend for the Intelligent Chatbot for Automated Examination system.

## Quick Start

### Windows

```powershell
cd backend
.\start.bat
```

### Linux/Mac

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Features

✅ **User Authentication** - Secure registration and login with password hashing  
✅ **AI Question Generation** - Dynamic question generation based on subject, difficulty, and marks  
✅ **Automated Evaluation** - MCQ, True/False auto-grading + NLP-based Viva evaluation  
✅ **Database Management** - SQLAlchemy ORM with support for SQLite, MySQL, PostgreSQL  
✅ **RESTful API** - Clean API endpoints with JSON responses  
✅ **CORS Enabled** - Frontend-backend communication ready  

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | User login |

### Exam Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate-questions` | Generate exam questions |
| POST | `/api/submit-exam` | Submit and evaluate exam |
| GET | `/api/exam-history/<email>` | Get user exam history |

## Database Schema

### Tables
- `users` - User accounts
- `subjects` - Exam subjects (AI, Networks, Graphics, Compiler)
- `questions` - Question bank
- `exams` - Exam sessions
- `exam_answers` - User answers
- `exam_results` - Exam results and analytics

## Configuration

Edit `config.py` for different environments:
- Development (default)
- Production
- Testing

## Tech Stack

- **Flask 2.3.2** - Web framework
- **SQLAlchemy 3.0.5** - ORM
- **Flask-CORS** - Cross-origin support
- **PyJWT** - Token authentication
- **Werkzeug** - Password hashing

## File Structure

```
backend/
├── app.py              # Main Flask application
├── models.py           # Database models
├── ai_generator.py     # AI question generator & evaluator
├── config.py           # Configuration settings
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── start.bat          # Windows startup script
└── .gitignore         # Git ignore rules
```

## Development

### Initialize Database

```bash
python init_db.py
```

### Run Development Server

```bash
python app.py
```

Server runs on `http://localhost:5000`

### Test API

```bash
# Using curl
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"pass123"}'
```

## AI Integration

The system supports integration with:
- OpenAI GPT (recommended)
- Hugging Face Transformers
- Custom NLP models

See `ai_generator.py` for integration guide.

## Production Deployment

1. Set `SECRET_KEY` environment variable
2. Use production database (MySQL/PostgreSQL)
3. Set `debug=False` in app.py
4. Use WSGI server (Gunicorn/uWSGI)

## License

Educational Project - Free to use and modify
