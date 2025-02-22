from functools import wraps

from flask import jsonify, request

from app.libs.authhelper import verify_token
from app.models.userModel import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            payload = verify_token(token)
            current_user = User.find_user_by_id(payload['user_id'])
            if not current_user:
                raise ValueError("User not found")
        except ValueError as e:
            return jsonify({'message': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated