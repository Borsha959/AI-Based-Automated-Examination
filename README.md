# Intelligent Chatbot for Automated Examination

A full-stack educational assessment platform that automates question generation, exam delivery, answer evaluation, and result analysis using AI.

This repository contains a complete student-facing web application, a Flask-based API backend, and AI-assisted evaluation workflows suitable for academic demonstrations, software engineering coursework, and capstone projects.

## Table of Contents

1. [Project Summary](#project-summary)
2. [Problem Statement](#problem-statement)
3. [Educational Objectives](#educational-objectives)
4. [Scope and Target Users](#scope-and-target-users)
5. [Key Features](#key-features)
6. [System Architecture](#system-architecture)
7. [Module-by-Module Explanation](#module-by-module-explanation)
8. [Assessment Model](#assessment-model)
9. [Question Generation and Evaluation Pipeline](#question-generation-and-evaluation-pipeline)
10. [Technology Stack](#technology-stack)
11. [Project Structure](#project-structure)
12. [How the System Works](#how-the-system-works)
13. [API Reference](#api-reference)
14. [Database Design](#database-design)
15. [Setup and Installation](#setup-and-installation)
16. [Environment Variables](#environment-variables)
17. [Execution and Testing](#execution-and-testing)
18. [Quality Attributes](#quality-attributes)
19. [Security Notes](#security-notes)
20. [Educational Significance](#educational-significance)
21. [Limitations and Future Scope](#limitations-and-future-scope)

## Project Summary

Traditional examinations require significant manual effort for question preparation, answer checking, and performance analysis. This project introduces an AI-enabled examination workflow that can:

- generate question papers dynamically,
- evaluate objective and descriptive responses automatically,
- calculate marks with configurable rules,
- and provide structured feedback for learning improvement.

The platform is designed to be explainable, modular, and practical for academic use.

## Problem Statement

Educational institutions often face challenges such as delayed result publication, inconsistent manual grading, and limited personalized feedback for students. In large classes, the workload on faculty increases significantly, especially when descriptive answers must be evaluated one by one.

This project addresses those issues by providing an intelligent examination workflow where:

- question papers are generated automatically based on selected constraints,
- objective answers are graded instantly using deterministic logic,
- short descriptive answers are evaluated through AI-assisted scoring,
- and complete result summaries are stored for review and analytics.

The system is intended to support fair, repeatable, and scalable assessment operations.

## Educational Objectives

The main objectives of this project are:

- automate end-to-end examination tasks,
- reduce teacher workload in repetitive evaluation activities,
- provide immediate and consistent scoring,
- support data-driven academic feedback,
- and demonstrate real-world integration of AI in educational technology.

## Scope and Target Users

### Scope

- Web-based examination workflow (frontend and backend)
- Authentication for students and administrator
- Dynamic question generation for selected subjects
- Mixed-format exam attempts (MCQ, True/False, Viva)
- Automatic evaluation and score computation
- Historical result retrieval and admin analytics

### Out of Scope

- Proctoring and anti-cheating detection
- Multi-institution tenant management
- Offline mobile app clients
- Advanced psychometric modeling

### Target Users

- Undergraduate students taking practice or formal internal exams
- Teachers and evaluators who need automated assistance
- Academic project reviewers and viva boards
- EdTech researchers evaluating AI-assisted assessment prototypes

## Key Features

### Student Features

- User registration and login
- Subject selection and exam setup
- Difficulty selection: Beginner, Intermediate, Pro
- Marks-based paper patterns: 25, 40, 60
- Mixed question paper (MCQ, True/False, Viva)
- Real-time timer with submission flow
- Detailed result sheet with per-question analysis
- Result PDF download
- Question paper PDF download

### Evaluation Features

- Automatic MCQ and True/False grading
- Negative marking for incorrect MCQ answers (-0.25)
- AI-based Viva evaluation
- Similarity-based fallback scoring if AI service is unavailable

### Admin Features

- Admin login workflow
- Dashboard statistics (users, exams, questions, average performance)
- User management with deletion support
- Exam monitoring view

## System Architecture

The application follows a layered architecture with clear separation of concerns:

- Presentation Layer: Single-page frontend in HTML, TailwindCSS, and JavaScript.
- Application Layer: Flask API endpoints orchestrating auth, question generation, and evaluation workflows.
- Domain/Data Layer: SQLAlchemy models and relational tables for users, exams, answers, and results.
- Intelligence Layer: Gemini-powered question and Viva evaluation engine with fallback behavior.

### Architectural Characteristics

- Stateless request-response API design for easier integration.
- Persistent relational storage for traceable exam history.
- Hybrid AI strategy combining deterministic grading and AI scoring.
- Graceful degradation via fallback logic when AI responses fail.

### Deployment Shape

- Frontend can be served as static file.
- Backend runs as Flask service on localhost for development.
- Database defaults to SQLite for easy academic setup.

## Module-by-Module Explanation

### Frontend Layer

- Handles user interfaces for registration, login, dashboard, exam attempt, results, and admin views.
- Sends API requests for all business actions.
- Manages timer lifecycle, answer capture, and page transitions.
- Generates downloadable PDFs for question papers and result reports.

### Backend API Layer

- Exposes REST endpoints for authentication and exam management.
- Applies business rules for marks, negative scoring, and result aggregation.
- Controls access to admin-only resources using token claims.

### AI Service Layer

- Generates balanced question sets according to selected exam pattern.
- Evaluates Viva responses using prompt-based scoring logic.
- Handles transient AI failures using retries and deterministic fallback generation.

### Data Layer

- Maintains normalized entities for users, subjects, questions, exams, answers, and final results.
- Enables historical reporting and admin-level analytics.

## Assessment Model

### Question Types

- MCQ: 1 mark each
- True/False: 1 mark each
- Viva/Short Answer: 2 marks each

### Current Exam Patterns

- 25 marks: 22 questions, 15 minutes
- 40 marks: 35 questions, 25 minutes
- 60 marks: 53 questions, 30 minutes

### Distribution Rules

- 25 marks: 15 MCQ, 3 Viva, 4 True/False
- 40 marks: 25 MCQ, 5 Viva, 5 True/False
- 60 marks: 40 MCQ, 7 Viva, 6 True/False

### Scoring Rules

- Correct objective answer: full marks
- Wrong MCQ answer: -0.25
- Wrong True/False answer: 0
- Viva score: AI-evaluated (0 to 2 range)

### Why This Model Is Educationally Useful

- Objective questions validate factual and conceptual clarity.
- Viva questions assess explanatory depth and understanding quality.
- Negative marking discourages random guessing in MCQ-based sections.
- Mixed distribution creates a balanced assessment of breadth and depth.

## Question Generation and Evaluation Pipeline

### A) Question Generation Pipeline

1. Student selects subject, marks, and difficulty.
2. Backend resolves an exam pattern (question count, duration, distribution).
3. AI prompt is generated with strict JSON output format and distribution rules.
4. AI response is parsed and validated.
5. Duplicate or malformed entries are filtered.
6. Missing quotas are completed with fallback question builders.
7. Final question set is stored and sent to frontend.

### B) Submission and Evaluation Pipeline

1. Student submits all captured answers.
2. Objective questions are matched against answer keys.
3. Viva responses are evaluated with AI rubric-based scoring.
4. If AI evaluation fails, similarity fallback scoring is applied.
5. Marks, counts, negative marks, and percentage are computed.
6. Result rows are stored and returned as a detailed response.

### C) Reliability Controls

- AI retry mechanism for rate-limited responses.
- Structured output validation before final acceptance.
- Fallback generation and fallback scoring for continuity.
- Defensive parsing for question option payloads.

## Technology Stack

### Frontend

- HTML5
- TailwindCSS (CDN)
- Vanilla JavaScript (ES6+)
- jsPDF for report generation

### Backend

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Werkzeug (password hashing)
- PyJWT (token handling)
- python-dotenv

### AI Integration

- Google Gemini API via google-genai
- Retry strategy for transient API failures
- Offline fallback question generation

### Database

- SQLite (default)
- ORM abstraction allows migration to MySQL/PostgreSQL

## Project Structure

```text
AI-Based-Automated-Examination/
|
|- index.html
|- README.md
|- QUICK_START.md
|- BACKEND_SETUP_GUIDE.md
|- PROJECT_INTRODUCTION.md
|- run-backend.bat
|
`- backend/
   |- app.py
   |- ai_generator.py
   |- models.py
   |- config.py
   |- init_db.py
   |- requirements.txt
   |- start.bat
   `- instance/
```

### Important Files and Responsibilities

- index.html: frontend pages, exam flow, timer, admin UI, and PDF export logic.
- backend/app.py: API routes, authentication, exam orchestration, scoring aggregation.
- backend/ai_generator.py: AI prompts, response parsing, deduplication, fallback logic.
- backend/models.py: SQLAlchemy schema and entity relationships.
- backend/init_db.py: database reset and bootstrap for default subjects.
- backend/start.bat: one-step backend startup script for Windows.

## How the System Works

### 1) Authentication

- Student registers through `POST /api/register`
- Student/admin logs in through `POST /api/login`
- Backend returns JWT token for authenticated operations

### 2) Exam Generation

- Student selects subject, marks, and difficulty
- Frontend calls `POST /api/generate-questions`
- Backend creates exam session and stores generated questions

### 3) Exam Attempt

- Questions are rendered in full-paper mode
- Timer starts based on selected pattern
- Student submits manually (or on timer completion)

### 4) Evaluation and Result

- Frontend calls `POST /api/submit-exam`
- Objective answers are checked directly
- Viva answers are evaluated through AI logic
- Result, percentage, and metadata are persisted

### 5) History and Admin Analytics

- Students can retrieve past attempts via `GET /api/exam-history/<email>`
- Admin dashboard reads statistics, users, and recent exams

### Typical Student Journey

1. Create account and sign in.
2. Choose a subject and exam configuration.
3. Attempt full paper within the timer window.
4. Submit and receive immediate evaluation.
5. Review detailed feedback and download report.

### Typical Admin Journey

1. Sign in with admin credentials.
2. Inspect platform-level stats.
3. Review users and recent examinations.
4. Remove invalid accounts if required.

## API Reference

### Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/register` | Register new student |
| POST | `/api/login` | Student/Admin login |

### Exam Management

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/generate-questions` | Create exam session and generate question set |
| POST | `/api/submit-exam` | Evaluate submitted answers and store result |
| GET | `/api/exam-history/<user_email>` | Retrieve student exam history |

### Admin

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/admin/overview` | Global dashboard stats |
| GET | `/api/admin/users` | User listing |
| GET | `/api/admin/exams` | Exam listing |
| DELETE | `/api/admin/users/<id>` | Delete user and related data |

### Example Request and Response

Generate exam request:

```json
{
  "subject": "Artificial Intelligence",
  "total_marks": 25,
  "difficulty": "Intermediate",
  "user_id": "student@example.com"
}
```

Submit exam request:

```json
{
  "user_id": "student@example.com",
  "answers": [
    { "question_id": 1, "answer": "A" },
    { "question_id": 2, "answer": "B" },
    { "question_id": 3, "answer": "A short explanatory answer" }
  ]
}
```

Result response (shape):

```json
{
  "total_marks": 18.75,
  "max_marks": 25,
  "correct_answers": 15,
  "wrong_answers": 7,
  "negative_marks": 1.25,
  "percentage": 75,
  "results": []
}
```

## Database Design

The system includes six core tables:

1. `users`: authentication and profile information
2. `subjects`: subject catalog
3. `questions`: generated question metadata and answer keys
4. `exams`: exam sessions
5. `exam_answers`: student answer records
6. `exam_results`: final result analytics

Relational design supports traceable exam sessions and post-exam reporting.

### Relationship Notes

- One user can have many exams.
- One exam belongs to one subject.
- One exam contains many answer rows.
- One exam has one final result row.
- One subject can be linked to many generated questions.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip
- Modern browser (Chrome, Edge, Firefox)
- VS Code recommended

### Windows (Recommended)

From project root:

```powershell
cd backend
.\start.bat
```

This script will:

- create a virtual environment if missing,
- install dependencies,
- and start the Flask server on `http://localhost:5000`.

Open frontend via one of the following:

- VS Code Live Server on `index.html`
- or Python HTTP server:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000`.

Alternative one-command launcher from project root:

```powershell
.\run-backend.bat
```

### Linux/Mac

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Environment Variables

Create `backend/.env` and configure at least the following:

```env
SECRET_KEY=replace-with-a-strong-secret
ADMIN_EMAIL=admin@examai.com
ADMIN_PASSWORD=change-this-password
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
```

Optional:

- `GEMINI_RETRIES` for retry attempts
- database URL overrides via config if needed

Recommended production-style values:

- Use a long random value for SECRET_KEY.
- Change default admin credentials before any real usage.
- Keep GEMINI_API_KEY outside source control.

## Execution and Testing

### Basic Test Checklist

1. Register a new student account
2. Log in and generate an exam
3. Answer mixed question types
4. Submit and verify result computation
5. Download question and result PDFs
6. Log in as admin and validate dashboard data

### Suggested Academic Demo Flow

1. Register two sample students.
2. Run one exam with 25 marks and one with 40 marks.
3. Demonstrate objective and Viva scoring differences.
4. Show negative marking effect with intentional wrong MCQs.
5. Present history and admin analytics screens.
6. Export and share PDF outputs as evidence.

### Troubleshooting Notes

- If backend is unreachable, verify API base URL and server port.
- If AI fails due to quota/rate limits, retry after a short delay.
- If database state is inconsistent during testing, run init_db.py to reset.
- If CORS errors appear, ensure backend is running and CORS is enabled.

## Quality Attributes

The current implementation targets the following software quality attributes:

- Usability: clean exam workflow with minimal user friction.
- Reliability: fallback mechanisms for AI-dependent operations.
- Maintainability: modular separation across frontend, API, AI, and data files.
- Traceability: complete exam and result persistence for review.
- Performance: objective grading is immediate; AI operations are isolated to generation and Viva scoring.

### Database Reset

To reinitialize schema and default subjects:

```powershell
cd backend
python init_db.py
```

## Security Notes

- Passwords are hashed before storage
- JWT is used for authenticated requests
- Admin APIs are protected with token checks
- For production, always use:
  - strong SECRET_KEY,
  - secure admin credentials,
  - HTTPS,
  - managed database backup strategy

## Educational Significance

This project demonstrates practical software engineering concepts across multiple domains:

- Web application development
- REST API design
- ORM-based relational modeling
- Applied AI integration in education
- Automated assessment strategies
- User-role management and authorization

It is suitable for:

- final year project demonstrations,
- classroom AI/SE labs,
- and institutional prototype discussions.

### Learning Outcomes for Students

By studying and presenting this project, learners can demonstrate:

- full-stack integration skills,
- applied API design and HTTP workflow understanding,
- database schema design and relational reasoning,
- practical AI integration with resilient fallback strategy,
- and software documentation and deployment literacy.

## Limitations and Future Scope

### Current Limitations

- Frontend is implemented as a single-page file
- AI quality depends on API availability and prompt behavior
- Anti-cheating mechanisms are not implemented

### Future Enhancements

- Adaptive difficulty based on student performance
- Voice-based exam interaction
- Multilingual support
- Advanced analytics dashboards
- LMS integration
- Proctoring and integrity monitoring

### Research and Productization Opportunities

- Compare AI scoring consistency with human evaluators.
- Add rubric-aware, topic-wise feedback generation.
- Introduce learning path recommendation from weak-topic trends.
- Add institution-level reporting and semester-wise analytics.
- Containerize services for cloud deployment.

---

This repository is maintained for educational and academic use.
