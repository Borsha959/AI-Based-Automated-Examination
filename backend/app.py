from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, User, Subject, Question, Exam, ExamAnswer, ExamResult
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
from functools import wraps

# Load .env BEFORE anything reads os.environ (e.g. ai_generator)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Project root is one level above this file (backend/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my-ai-exam-secret-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@examai.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Initialize extensions
db.init_app(app)
CORS(app)

# ==================== SERVE FRONTEND ====================

@app.route('/')
def index():
    return send_from_directory(PROJECT_ROOT, 'index.html')


@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Import AI question generator
from ai_generator import generate_questions_ai, evaluate_answer_ai

EXAM_PATTERNS = {
    25: {
        'total_questions': 22,
        'duration_minutes': 15,
        'distribution': {'MCQ': 15, 'Viva': 3, 'True/False': 4}
    },
    40: {
        'total_questions': 35,
        'duration_minutes': 25,
        'distribution': {'MCQ': 25, 'Viva': 5, 'True/False': 5}
    },
    60: {
        'total_questions': 53,
        'duration_minutes': 30,
        'distribution': {'MCQ': 40, 'Viva': 7, 'True/False': 6}
    }
}


def _decode_bearer_token():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ', 1)[1].strip()
    if not token:
        return None

    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        payload = _decode_bearer_token()
        if not payload or not payload.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# ==================== AUTHENTICATION ====================

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not name or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Dedicated admin login (credentials from backend/.env)
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            token = jwt.encode({
                'is_admin': True,
                'admin_email': ADMIN_EMAIL,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'message': 'Admin login successful',
                'token': token,
                'user': {
                    'id': 0,
                    'name': 'Administrator',
                    'email': ADMIN_EMAIL,
                    'is_admin': True
                }
            }), 200
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'is_admin': False,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'is_admin': False
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== QUESTION GENERATION ====================

@app.route('/api/generate-questions', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        subject = data.get('subject')
        total_marks = int(data.get('total_marks', 25))
        difficulty = data.get('difficulty', 'Intermediate')
        user_email = data.get('user_id')
        exam_pattern = EXAM_PATTERNS.get(total_marks)

        if not exam_pattern:
            return jsonify({'error': 'Invalid total marks. Please choose 25, 40, or 60.'}), 400
        
        # Get user
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get subject
        subject_obj = Subject.query.filter_by(name=subject).first()
        if not subject_obj:
            # Create subject if not exists
            subject_obj = Subject(name=subject, description=f"{subject} topics")
            db.session.add(subject_obj)
            db.session.commit()
        
        # Create exam session
        exam = Exam(
            user_id=user.id,
            subject_id=subject_obj.id,
            total_marks=total_marks,
            difficulty=difficulty,
            start_time=datetime.utcnow()
        )
        db.session.add(exam)
        db.session.commit()
        
        # Generate questions using AI
        try:
            questions_data = generate_questions_ai(subject, total_marks, difficulty, exam_pattern)
        except RuntimeError as ai_err:
            db.session.rollback()
            msg = str(ai_err)
            if "RATE_LIMIT_EXCEEDED" in msg:
                return jsonify({'error': 'The AI service is temporarily busy due to high demand. Please wait a moment and try again.'}), 503
            elif "INVALID_API_KEY" in msg:
                return jsonify({'error': 'AI service configuration error. Please contact the administrator.'}), 500
            return jsonify({'error': f'AI failed to generate questions: {msg}'}), 500
        
        questions_response = []
        for q_data in questions_data:
            # Save question to database
            question = Question(
                subject_id=subject_obj.id,
                question_text=q_data['question'],
                question_type=q_data['type'],
                options=json.dumps(q_data.get('options', [])),
                correct_answer=q_data['correct_answer'],
                explanation=q_data.get('explanation', ''),
                marks=q_data['marks'],
                difficulty=difficulty,
                topic=q_data.get('topic', '')
            )
            db.session.add(question)
            db.session.flush()
            
            # Link question to exam
            exam_answer = ExamAnswer(
                exam_id=exam.id,
                question_id=question.id
            )
            db.session.add(exam_answer)
            
            questions_response.append({
                'id': question.id,
                'question': question.question_text,
                'type': question.question_type,
                'options': json.loads(question.options) if question.options else [],
                'marks': question.marks,
                'topic': question.topic
            })
        
        db.session.commit()
        
        return jsonify({
            'exam_id': exam.id,
            'questions': questions_response,
            'exam_pattern': exam_pattern
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== EXAM SUBMISSION ====================

@app.route('/api/submit-exam', methods=['POST'])
def submit_exam():
    try:
        data = request.get_json()
        user_email = data.get('user_id')
        answers = data.get('answers', [])
        
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get latest exam
        exam = Exam.query.filter_by(user_id=user.id).order_by(Exam.id.desc()).first()
        if not exam:
            return jsonify({'error': 'No active exam found'}), 404
        
        # Update exam end time
        exam.end_time = datetime.utcnow()
        
        total_marks = 0
        correct_count = 0
        wrong_count = 0
        negative_marks = 0
        max_marks = 0
        
        results_details = []
        
        for ans_data in answers:
            question_id = ans_data.get('question_id')
            user_answer = ans_data.get('answer', '').strip()
            
            question = Question.query.get(question_id)
            if not question:
                continue

            question_options = []
            if question.options:
                try:
                    question_options = json.loads(question.options)
                except (TypeError, json.JSONDecodeError):
                    question_options = []
            
            max_marks += question.marks
            is_correct = False
            awarded_marks = 0
            
            # Evaluate answer
            if question.question_type == 'MCQ' or question.question_type == 'True/False':
                is_correct = user_answer.upper() == question.correct_answer.upper()
                if is_correct:
                    awarded_marks = question.marks
                    correct_count += 1
                else:
                    if question.question_type == 'MCQ' and user_answer:
                        negative_marks += 0.25
                        awarded_marks = -0.25
                    wrong_count += 1
            
            elif question.question_type == 'Viva':
                # Use AI to evaluate Viva answer
                ai_evaluation = evaluate_answer_ai(
                    question.question_text,
                    question.correct_answer,
                    user_answer
                )
                awarded_marks = ai_evaluation['marks']
                is_correct = ai_evaluation['is_correct']
                if is_correct:
                    correct_count += 1
                else:
                    wrong_count += 1
            
            total_marks += awarded_marks
            
            # Update exam answer
            exam_answer = ExamAnswer.query.filter_by(
                exam_id=exam.id,
                question_id=question_id
            ).first()
            
            if exam_answer:
                exam_answer.user_answer = user_answer
                exam_answer.is_correct = is_correct
                exam_answer.marks_awarded = awarded_marks
            
            results_details.append({
                'question_id': question_id,
                'question': question.question_text,
                'question_type': question.question_type,
                'question_marks': question.marks,
                'options': question_options,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'marks_awarded': awarded_marks,
                'explanation': question.explanation
            })
        
        # Calculate percentage
        percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
        
        # Save result
        result = ExamResult(
            exam_id=exam.id,
            total_marks=total_marks,
            max_marks=max_marks,
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            negative_marks=negative_marks,
            percentage=percentage
        )
        db.session.add(result)
        db.session.commit()
        
        return jsonify({
            'total_marks': round(total_marks, 2),
            'max_marks': max_marks,
            'correct_answers': correct_count,
            'wrong_answers': wrong_count,
            'negative_marks': round(negative_marks, 2),
            'percentage': round(percentage, 2),
            'results': results_details
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== EXAM HISTORY ====================

@app.route('/api/exam-history/<user_email>', methods=['GET'])
def get_exam_history(user_email):
    try:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        exams = Exam.query.filter_by(user_id=user.id).order_by(Exam.start_time.desc()).all()
        
        history = []
        for exam in exams:
            result = ExamResult.query.filter_by(exam_id=exam.id).first()
            subject = Subject.query.get(exam.subject_id)
            
            if result:
                history.append({
                    'exam_id': exam.id,
                    'subject': subject.name if subject else 'Unknown',
                    'total_marks': result.total_marks,
                    'max_marks': result.max_marks,
                    'percentage': result.percentage,
                    'date': exam.start_time.strftime('%Y-%m-%d %H:%M'),
                    'difficulty': exam.difficulty
                })
        
        return jsonify({'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ADMIN PANEL ====================

@app.route('/api/admin/overview', methods=['GET'])
@admin_required
def admin_overview():
    try:
        total_users = User.query.count()
        total_subjects = Subject.query.count()
        total_exams = Exam.query.count()
        total_questions = Question.query.count()
        total_results = ExamResult.query.count()

        avg_percentage = db.session.query(db.func.avg(ExamResult.percentage)).scalar() or 0

        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_subjects': total_subjects,
                'total_exams': total_exams,
                'total_questions': total_questions,
                'total_results': total_results,
                'average_percentage': round(float(avg_percentage), 2)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users', methods=['GET'])
@admin_required
def admin_users():
    try:
        users = User.query.order_by(User.created_at.desc()).all()
        data = []
        for user in users:
            exam_count = Exam.query.filter_by(user_id=user.id).count()
            data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M'),
                'exam_count': exam_count
            })
        return jsonify({'users': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/exams', methods=['GET'])
@admin_required
def admin_exams():
    try:
        exams = Exam.query.order_by(Exam.start_time.desc()).all()
        data = []
        for exam in exams:
            user = User.query.get(exam.user_id)
            subject = Subject.query.get(exam.subject_id)
            result = ExamResult.query.filter_by(exam_id=exam.id).first()

            data.append({
                'exam_id': exam.id,
                'student_name': user.name if user else 'Unknown',
                'student_email': user.email if user else 'Unknown',
                'subject': subject.name if subject else 'Unknown',
                'difficulty': exam.difficulty,
                'date': exam.start_time.strftime('%Y-%m-%d %H:%M'),
                'status': 'Completed' if result else 'In Progress',
                'score': f"{round(result.total_marks, 2)}/{result.max_marks}" if result else 'N/A',
                'percentage': round(result.percentage, 2) if result else None
            })

        return jsonify({'exams': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== INITIALIZE DATABASE ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    print("\n" + "="*50)
    print("  AI Examination System is RUNNING")
    print("  Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
