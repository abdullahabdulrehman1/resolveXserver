import logging

from flask import jsonify

from app.libs.authhelper import generate_refresh_token, generate_token
from app.models.userModel import User
from app.schemas.user_schema import LoginSchema

logger = logging.getLogger(__name__)


def login(data):
    # Validate input data using LoginSchema
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        logger.warning(f"Validation errors: {errors}")
        return jsonify({"errors": errors}), 400

    user = User.check_user(data["email"], data["password"])
    if not user:
        logger.warning(f"Failed login attempt for email: {data['email']}")
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate tokens using authhelper
    access_token = generate_token(user)
    refresh_token = generate_refresh_token(user)

    # Validate token structure
    token_parts = access_token.split(".")
    print(f"Generated token: {access_token}")  # Temporary debug line
    assert len(token_parts) == 3, "Invalid token generated"
    if len(token_parts) != 3:
        logger.error("Generated invalid JWT structure")
        raise ValueError("Malformed token generated")

    logger.debug(f"Token header: {token_parts[0]}")
    logger.info(f"Successful login for: {user['email']}")

    return jsonify(
        {"access_token": access_token, "refresh_token": refresh_token, "user": user}
    )
