from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Task, Category, Bid
from utils import role_required

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.serialize() for task in tasks])

@task_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('poster')
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()
    task = Task(
        title=data['title'],
        description=data['description'],
        payment=data['payment'],
        location=data['location'],
        poster_id=user_id
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"}), 201

@task_bp.route('/<int:task_id>/start', methods=['PATCH'])
@jwt_required()
@role_required('doer')
def start_task(task_id):
    task = Task.query.get(task_id)
    if task.status != "Pending":
        return jsonify({"error": "Task is already in progress or completed"}), 400

    task.status = "In Progress"
    db.session.commit()

    return jsonify({"message": "Task started"}), 200

@task_bp.route('/<int:task_id>/complete', methods=['PATCH'])
@jwt_required()
@role_required('doer')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task.status != "In Progress":
        return jsonify({"error": "Task must be in progress to complete"}), 400

    task.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Task marked as completed"}), 200

@task_bp.route('/filter', methods=['GET'])
def filter_tasks():
    poster_id = request.args.get('poster_id')
    doer_id = request.args.get('doer_id')
    status = request.args.get('status')

    query = Task.query

    if poster_id:
        query = query.filter_by(poster_id=poster_id)
    if doer_id:
        query = query.filter_by(doer_id=doer_id)
    if status:
        query = query.filter_by(status=status)

    tasks = query.all()

    return jsonify([{
        'title': task.title,
        'description': task.description,
        'payment': task.payment,
        'status': task.status,
        'posted_on': task.posted_on
    } for task in tasks]), 200

@task_bp.route('/<int:task_id>/bid', methods=['POST'])
@jwt_required()
def place_bid(task_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    amount = data.get('amount')
    
    bid = Bid(
        amount=amount,
        task_id=task_id,
        user_id=current_user_id
    )
    
    db.session.add(bid)
    db.session.commit()

    return jsonify({'message': 'Bid placed successfully'}), 201

# Route for selecting a bid
@task_bp.route('/<int:task_id>/select_bid/<int:bid_id>', methods=['PATCH'])
@jwt_required()
def select_bid(task_id, bid_id):
    task = Task.query.get_or_404(task_id)
    bid = Bid.query.get_or_404(bid_id)

    task.doer_id = bid.user_id  # Select the bidder as the doer
    db.session.commit()

    return jsonify({'message': 'Bid selected successfully'}), 200


@task_bp.route('/search', methods=['GET'])
def search_tasks():
    keyword = request.args.get('q')
    tasks = Task.query.filter(Task.title.ilike(f"%{keyword}%") | Task.description.ilike(f"%{keyword}%")).all()
    
    return jsonify([{
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'posted_on': task.posted_on
    } for task in tasks]), 200

@task_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.name for category in categories]), 200

