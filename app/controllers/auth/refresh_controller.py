from flask import jsonify
from app.models.userModel import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.libs.error_helper import handle_error

@jwt_required(refresh=True)
def refresh_access_token():
    try:
        # Get the user ID from the refresh token
        current_user_id = get_jwt_identity()

        # Verify if user still exists
        user = User.find_user_by_id(current_user_id)
        if not user:
            return handle_error("User not found", 404)

        # Generate new access & refresh tokens
        new_access_token = create_access_token(identity=current_user_id)
        new_refresh_token = create_refresh_token(identity=current_user_id)

        return jsonify({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }), 200

    except Exception as e:
        return handle_error(f"Something went wrong: {str(e)}", 500)