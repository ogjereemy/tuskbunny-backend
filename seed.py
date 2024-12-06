from db import db
from app import app
from models import User, Task, Review
from werkzeug.security import generate_password_hash
from datetime import datetime

# Sample users, tasks, and reviews
def seed_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create sample users
        user1 = User(username='john_doe', email='john@example.com', password_hash=generate_password_hash('password123'), role='poster')
        user2 = User(username='jane_doe', email='jane@example.com', password_hash=generate_password_hash('password123'), role='doer')
        user3 = User(username='alice_smith', email='alice@example.com', password_hash=generate_password_hash('password123'), role='poster')

        # Add users to session
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        # Commit changes
        db.session.commit()

        # Create some tasks
        task1 = Task(title='Fix a leaky faucet', description='Need someone to fix a leaky faucet in the kitchen.', payment=50.0, posted_on=datetime.utcnow(), poster_id=user1.id)
        task2 = Task(title='Deliver groceries', description='Pick up groceries and deliver them to the customer.', payment=30.0, posted_on=datetime.utcnow(), poster_id=user3.id)

        # Add tasks to session
        db.session.add(task1)
        db.session.add(task2)

        # Commit changes
        db.session.commit()

        # Create some reviews
        review1 = Review(rating=5, comment="Excellent job!", reviewer_id=user1.id, task_id=task1.id)
        review2 = Review(rating=4, comment="Good work, but late.", reviewer_id=user3.id, task_id=task2.id)

        # Add reviews to session
        db.session.add(review1)
        db.session.add(review2)

        # Commit changes
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
