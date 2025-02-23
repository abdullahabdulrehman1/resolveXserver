from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.libs.error_helper import handle_error
from app.models.userModel import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            # Fetch the user from the database
            current_user = User.find_user_by_id(current_user_id)
            if not current_user:
                return handle_error("User not found", 404)
        except Exception as e:
            return handle_error(str(e), 401)

        return f(current_user, *args, **kwargs)
    return decorated