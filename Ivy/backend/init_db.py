from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
import os
import random

from database import SessionLocal, engine
from models import Base, User, Message, Feedback, ProgressTrack
from security import get_password_hash

# Create all tables
Base.metadata.create_all(bind=engine)

def init_db(db: Session) -> None:
    # Check if we already have users
    if db.query(User).first():
        return

    # Create sample users
    sample_users = [
        {
            "email": "john@example.com",
            "name": "John Doe",
            "password": "password123",
            "selected_role": "frontend"
        },
        {
            "email": "jane@example.com",
            "name": "Jane Smith",
            "password": "password456",
            "selected_role": "backend"
        }
    ]

    for user_data in sample_users:
        user = User(
            email=user_data["email"],
            name=user_data["name"],
            hashed_password=get_password_hash(user_data["password"]),
            selected_role=user_data["selected_role"]
        )
        db.add(user)
    db.commit()

    # Add sample progress data
    sample_topics = [
        "Data Structures",
        "Algorithms",
        "System Design",
        "JavaScript",
        "Python",
        "SQL",
        "React",
        "Node.js"
    ]

    users = db.query(User).all()
    for user in users:
        for topic in sample_topics:
            progress = ProgressTrack(
                user_id=user.id,
                topic=topic,
                progress=round(random.random(), 2),
                last_studied=datetime.utcnow() - timedelta(days=random.randint(0, 10))
            )
            db.add(progress)
    db.commit()

    # Add sample chat messages
    sample_questions = [
        "What are the key differences between var, let, and const in JavaScript?",
        "Can you explain how React's virtual DOM works?",
        "What is the time complexity of quicksort?",
        "How would you design a scalable chat application?"
    ]

    for user in users:
        for question in sample_questions:
            # User message
            user_message = Message(
                user_id=user.id,
                role="user",
                content=question,
                timestamp=datetime.utcnow() - timedelta(minutes=random.randint(1, 1000)),
                question_type="technical"
            )
            db.add(user_message)
            db.commit()

            # Assistant message
            assistant_message = Message(
                user_id=user.id,
                role="assistant",
                content=f"Here's a detailed explanation about {question.lower()}...",
                timestamp=user_message.timestamp + timedelta(seconds=2),
                question_type="technical"
            )
            db.add(assistant_message)

            # Add feedback
            feedback = Feedback(
                message_id=assistant_message.id,
                rating=random.randint(3, 5),
                was_helpful=True,
                comment="Very helpful explanation!",
                created_at=assistant_message.timestamp + timedelta(minutes=1)
            )
            db.add(feedback)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
        print("Database initialized successfully!")
    finally:
        db.close() 