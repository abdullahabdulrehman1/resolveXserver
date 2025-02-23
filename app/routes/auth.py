from flask import Blueprint, request, jsonify,current_app
from flask_jwt_extended import jwt_required
from app.controllers.auth.login_controller import login
from app.controllers.auth.get_user_controller import get_user
from app.controllers.auth.refresh_controller import refresh_access_token
from app.controllers.auth.register_controller import register
from app.controllers.auth.reset_password_controller import request_password_reset, reset_password
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

@auth_bp.route('/user', methods=['GET'])
@token_required
def get_user_route(current_user):
    return get_user(current_user)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token_route():
    return refresh_access_token()

@auth_bp.route('/request_password_reset', methods=['POST'])
def request_password_reset_route():
    return request_password_reset()

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password_route():
    return reset_password()
@auth_bp.route('/verify_env', methods=['GET'])
def verify_env():
    api_key = current_app.config.get('MAILJET_API_KEY')
    api_secret = current_app.config.get('MAILJET_API_SECRET')
    sender = current_app.config.get('MAILJET_SENDER')
    return jsonify({
        "MAILJET_API_KEY": api_key,
        "MAILJET_API_SECRET": api_secret,
        "MAILJET_SENDER": sender
    })