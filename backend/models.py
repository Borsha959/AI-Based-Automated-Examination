from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    exams = db.relationship('Exam', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='subject', lazy=True, cascade='all, delete-orphan')
    exams = db.relationship('Exam', backref='subject', lazy=True)
    
    def __repr__(self):
        return f'<Subject {self.name}>'


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # MCQ, Viva, True/False
    options = db.Column(db.Text)  # JSON string for options
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    marks = db.Column(db.Float, default=1.0)
    difficulty = db.Column(db.String(20))  # Beginner, Intermediate, Pro
    topic = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    exam_answers = db.relationship('ExamAnswer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_type}>'


class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    
    # Relationships
    answers = db.relationship('ExamAnswer', backref='exam', lazy=True, cascade='all, delete-orphan')
    result = db.relationship('ExamResult', backref='exam', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Exam {self.id}: User {self.user_id}>'


class ExamAnswer(db.Model):
    __tablename__ = 'exam_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)
    marks_awarded = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExamAnswer {self.id}: Exam {self.exam_id}>'


class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, unique=True)
    total_marks = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    negative_marks = db.Column(db.Float, default=0.0)
    percentage = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExamResult {self.id}: {self.percentage}%>'
