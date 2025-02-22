from flask import Blueprint, jsonify, request
from app.controllers.auth.register_controller import register
from app.controllers.auth.login_controller import login
from app.controllers.auth.get_user_controller import get_user
from app.middlewares.auth_middleware import token_required
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@auth_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    return login(data)
@token_required
@auth_bp.route('/user', methods=['GET'])
def get_user_route():
    return get_user()