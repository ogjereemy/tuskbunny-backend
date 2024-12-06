from db import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'poster' or 'doer'

    tasks_posted = db.relationship('Task', backref='poster', foreign_keys='Task.poster_id')
    tasks_assigned = db.relationship('Task', backref='doer', foreign_keys='Task.doer_id')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    payment = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    location = db.Column(db.String(120))
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    deadline = db.Column(db.DateTime, nullable=True)
    scheduled_for = db.Column(db.DateTime, nullable=True)  # Future scheduling

    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Task doer (once accepted)

    # poster = db.relationship('User', backref=db.backref('tasks_posted', lazy=True), foreign_keys=[poster_id])
    # doer = db.relationship('User', backref=db.backref('tasks_assigned', lazy=True), foreign_keys=[doer_id])

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Rating from 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    
    # Foreign keys
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

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
    
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    task = db.relationship('Task', backref='payment')
    payer = db.relationship('User', foreign_keys=[payer_id], backref='payments_made')
    payee = db.relationship('User', foreign_keys=[payee_id], backref='payments_received')

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='notifications')

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    tasks = db.relationship('Task', backref='category')

class Bid(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    task = db.relationship('Task', backref='bids')
    user = db.relationship('User', backref='bids')
