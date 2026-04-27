"""
Database initialization script
Run this to create/reset the database
"""

from app import app, db
from models import User, Subject, Question, Exam, ExamAnswer, ExamResult

def init_database():
    """Initialize database and create all tables"""
    with app.app_context():
        # Drop all tables (careful in production!)
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating new tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Add default subjects
        print("\nAdding default subjects...")
        subjects = [
            Subject(name='Artificial Intelligence', description='AI, ML, and Deep Learning topics'),
            Subject(name='Computer Networks', description='Networking protocols and concepts'),
            Subject(name='Computer Graphics', description='Graphics algorithms and visualization'),
            Subject(name='Compiler Design', description='Compiler construction and design')
        ]
        
        for subject in subjects:
            db.session.add(subject)
        
        db.session.commit()
        print("✓ Default subjects added!")
        
        # Display summary
        print("\n" + "="*50)
        print("DATABASE INITIALIZED SUCCESSFULLY")
        print("="*50)
        print(f"Tables created: {len(db.metadata.tables)}")
        print(f"Subjects added: {Subject.query.count()}")
        print("\nYou can now run the application with:")
        print("  python app.py")
        print("="*50)

if __name__ == '__main__':
    init_database()
