import logging
from flask import jsonify
from app.libs.error_helper import handle_error

logger = logging.getLogger(__name__)

def get_user(current_user):
    try:
        # Convert ObjectId to string for JSON serialization
        current_user["_id"] = str(current_user["_id"])

        logger.info(f"✅ User Data Found: {current_user}")
        return jsonify({"user": current_user}), 200

    except Exception as e:
        logger.error(f"❌ Error fetching user data: {str(e)}")
        return handle_error("Something went wrong. Please try again later", 500)