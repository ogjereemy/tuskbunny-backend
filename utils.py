from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models import User
from flask import jsonify

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role != required_role:
                return jsonify({"error": "You are not authorized to perform this action"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
