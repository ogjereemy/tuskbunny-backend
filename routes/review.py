from flask import Blueprint, request, jsonify
from db import db
from models import Review, Task, User
from flask_jwt_extended import jwt_required, get_jwt_identity

review_bp = Blueprint('reviews', __name__)

# Post a review
@review_bp.route('/<int:task_id>/add', methods=['POST'])
@jwt_required()
def add_review(task_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    rating = data.get('rating')
    comment = data.get('comment', '')

    task = Task.query.get_or_404(task_id)

    if task.doer_id != current_user_id and task.poster_id != current_user_id:
        return jsonify({'error': 'You can only review tasks you were involved in'}), 403

    reviewee_id = task.poster_id if task.doer_id == current_user_id else task.doer_id

    review = Review(
        rating=rating,
        comment=comment,
        reviewer_id=current_user_id,
        reviewee_id=reviewee_id,
        task_id=task.id
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully'}), 201

# Get reviews for a user
@review_bp.route('/user/<int:user_id>', methods=['GET'])
def get_reviews_for_user(user_id):
    reviews = Review.query.filter_by(reviewee_id=user_id).all()
    return jsonify([{
        'rating': review.rating,
        'comment': review.comment,
        'reviewer': review.reviewer.username,
        'task_id': review.task_id,
        'created_at': review.created_at
    } for review in reviews]), 200
