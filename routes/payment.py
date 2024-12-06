from flask import Blueprint, request, jsonify
from db import db
from models import Payment, Task, User
from flask_jwt_extended import jwt_required, get_jwt_identity

payment_bp = Blueprint('payments', __name__)

# Create a payment
@payment_bp.route('/task/<int:task_id>/pay', methods=['POST'])
@jwt_required()
def create_payment(task_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    amount = data.get('amount')

    task = Task.query.get_or_404(task_id)

    if task.poster_id != current_user_id:
        return jsonify({'error': 'Only the task poster can make a payment'}), 403

    if task.doer_id is None:
        return jsonify({'error': 'Task does not have a doer yet'}), 400

    payment = Payment(
        amount=amount,
        task_id=task.id,
        payer_id=current_user_id,
        payee_id=task.doer_id,
        status='Pending'
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({'message': 'Payment initiated successfully'}), 201

# Update payment status
@payment_bp.route('/<int:payment_id>/update', methods=['PATCH'])
@jwt_required()
def update_payment_status(payment_id):
    data = request.get_json()
    status = data.get('status')

    payment = Payment.query.get_or_404(payment_id)

    payment.status = status
    db.session.commit()

    return jsonify({'message': 'Payment status updated successfully'}), 200
