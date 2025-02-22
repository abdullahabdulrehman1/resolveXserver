from flask import jsonify, request
from app.models.userModel import User
from app.libs.authhelper import verify_token
import logging

logger = logging.getLogger(__name__)


def get_user():
    try:
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        current_user_id = payload["user_id"]

        print(f"🔍 Looking up user with ID: {current_user_id}")  # Debugging

        # Fetch user using the corrected method
        user = User.find_user_by_id(current_user_id)

        if not user:
            logger.warning("❌ User not found")
            return jsonify({"error": "User not found"}), 404

        # Convert ObjectId to string
        user["_id"] = str(user["_id"])

        print("✅ User Data Found:", user)  # Debugging
        return jsonify({"user": user}), 200

    except Exception as e:
        logger.error(f"❌ Error fetching user data: {str(e)}")
        return jsonify({"error": "Something went wrong. Please try again later"}), 500
