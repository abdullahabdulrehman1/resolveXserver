import logging
from flask import jsonify
from app.models.userModel import User
from app.schemas.user_schema import LoginSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from app.libs.error_helper import handle_error

logger = logging.getLogger(__name__)

def login(data):
    try:
        # Validate input data using LoginSchema
        schema = LoginSchema()
        errors = schema.validate(data)
        if errors:
            logger.warning(f"Validation errors: {errors}")
            return handle_error("Validation errors", 400)

        user = User.check_user(data["email"], data["password"])
        if not user:
            logger.warning(f"Failed login attempt for email: {data['email']}")
            return handle_error("Invalid credentials", 401)

        # Convert ObjectId to string for JSON serialization
        user_id = str(user["_id"])

        # Generate tokens using authhelper
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user_id)

        # Validate token structure
        token_parts = access_token.split(".")
        print(f"Generated token: {access_token}")  # Temporary debug line
        assert len(token_parts) == 3, "Invalid token generated"
        if len(token_parts) != 3:
            logger.error("Generated invalid JWT structure")
            raise ValueError("Malformed token generated")

        logger.debug(f"Token header: {token_parts[0]}")
        logger.info(f"Successful login for: {user['email']}")

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        })
    except Exception as e:
        logger.error(f"❌ Error during login: {str(e)}")
        return handle_error("Something went wrong. Please try again later", 500)