from flask import Blueprint, jsonify
from db import db
from models import Notification
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_bp = Blueprint('notifications', __name__)

# Get notifications for the logged-in user
@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=current_user_id).all()

    return jsonify([{
        'message': notification.message,
        'created_at': notification.created_at,
        'is_read': notification.is_read
    } for notification in notifications]), 200

# Mark a notification as read
@notification_bp.route('/<int:notification_id>/mark_read', methods=['PATCH'])
@jwt_required()
def mark_notification_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    notification.is_read = True
    db.session.commit()

    return jsonify({'message': 'Notification marked as read'}), 200
