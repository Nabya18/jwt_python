from functools import wraps
from flask import request, jsonify


def create_token_required_decorator(auth_service):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token missing'}), 401

            try:
                token = token.split(' ')[1]  # Remove 'Bearer ' prefix
                user = auth_service.validate_token(token)
                request.current_user = user
            except Exception as e:
                return jsonify({'message': 'Invalid token'}), 401

            return f(*args, **kwargs)

        return decorated

    return token_required