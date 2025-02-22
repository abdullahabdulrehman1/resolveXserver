from flask import Blueprint, request, jsonify
from app.models.userModel import User
from app.libs.authhelper import generate_token, verify_refresh_token

refresh_bp = Blueprint('refresh', __name__)

@refresh_bp.route('', methods=['POST'])
def refresh_access_token():
    refresh_token = request.json.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'message': 'Refresh token required'}), 400

    try:
        payload = verify_refresh_token(refresh_token)
        user = User.find_user_by_id(payload['user_id'])
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        new_access_token = generate_token(user)
        return jsonify({'access_token': new_access_token}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 401