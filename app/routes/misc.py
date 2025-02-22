from flask import Blueprint

misc_bp = Blueprint("misc", __name__)

@misc_bp.route("/test", methods=["GET"])
def test_route():
    from app import mongo  # Import inside the function to avoid circular import
    return {"message": "MongoDB is connected!"}
