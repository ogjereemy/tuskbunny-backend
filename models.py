from enum import Enum
from datetime import datetime
from db import db

class UserRole(Enum):
    POSTER = "POSTER"
    DOER = "DOER"

class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    tasks_posted = db.relationship('Task', backref='task_creator', foreign_keys='Task.poster_id', lazy='select')
    tasks_assigned = db.relationship('Task', backref='task_assignee', foreign_keys='Task.doer_id', lazy='select')
    bids = db.relationship('Bid', backref='bidder', lazy='select')

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    payment = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    location = db.Column(db.String(120))
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the category relationship if applicable
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    scheduled_for = db.Column(db.DateTime, nullable=True)

    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    category = db.relationship('Category', backref='categories')
    poster = db.relationship('User', foreign_keys=[poster_id], backref='posted_tasks')  # Renamed backref
    doer = db.relationship('User', foreign_keys=[doer_id], backref='assigned_tasks')


class Bid(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('task_id', 'user_id', name='_task_user_uc'),)

    task = db.relationship('Task', backref='bids')
    user = db.relationship('User', backref='user_bids')


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    tasks = db.relationship('Task', backref='task_category')


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Rating from 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    
    # Foreign keys
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    # Relationships
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given')
    reviewee = db.relationship('User', foreign_keys=[reviewee_id], backref='reviews_received')
    task = db.relationship('Task', backref='reviews')


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., 'Pending', 'Completed', etc.
    
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    task = db.relationship('Task', backref='task_payment')
    payer = db.relationship('User', foreign_keys=[payer_id], backref='payments_made')
    payee = db.relationship('User', foreign_keys=[payee_id], backref='payments_received')

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f"<Notification(id={self.id}, message={self.message}, user_id={self.user_id})>"
