from app import app
from db import db
from models import User, Task, Review, Payment, Category, Bid, UserRole, Notification

from datetime import datetime, timedelta


# Create seed data
def seed_data():
    with app.app_context():
        # Drop all existing tables and recreate them
        db.drop_all()  # Drop all tables before creating new ones
        db.create_all()  # Create the tables again
        
        # Seed categories
        category1 = Category(name="Home Services")
        category2 = Category(name="Delivery")
        category3 = Category(name="Personal Assistance")
        db.session.add_all([category1, category2, category3])

        # Seed users
        user1 = User(username="john_doe", email="john@example.com", password_hash="hashedpassword1", role=UserRole.POSTER)
        user2 = User(username="jane_smith", email="jane@example.com", password_hash="hashedpassword2", role=UserRole.DOER)
        db.session.add_all([user1, user2])

        # Seed tasks
        task1 = Task(
            title="Fix the sink",
            description="Need someone to fix the kitchen sink.",
            payment=50.0,
            location="123 Main St",
            deadline=datetime.utcnow() + timedelta(days=3),
            poster=user1,
            category=category1
        )
        task2 = Task(
            title="Grocery delivery",
            description="Deliver groceries from the store to my home.",
            payment=20.0,
            location="456 Elm St",
            deadline=datetime.utcnow() + timedelta(days=1),
            poster=user1,
            doer=user2,
            category=category2
        )
        db.session.add_all([task1, task2])

        # Seed reviews
        review1 = Review(rating=5, comment="Great service!", reviewer=user1, reviewee=user2, task=task2)
        db.session.add(review1)

        # Seed payments
        payment1 = Payment(amount=50.0, status="Completed", task=task1, payer=user1, payee=user2)
        db.session.add(payment1)

        # Seed notifications
        notification1 = Notification(message="You have a new task assigned", user=user2)
        db.session.add(notification1)

        # Seed bids
        bid1 = Bid(amount=45.0, task=task1, user=user2)
        db.session.add(bid1)

        # Commit the session
        db.session.commit()
        print("Seed data inserted successfully!")

# Run the seed function
if __name__ == "__main__":
    seed_data()
