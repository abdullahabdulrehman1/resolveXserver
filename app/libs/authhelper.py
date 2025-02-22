import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user):
    payload = {
        'user_id': str(user['_id']),
        'email': user['email'],
        'user_type': user['user_type'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def verify_refresh_token(refresh_token):
    """Verify refresh token validity"""
    try:
        payload = jwt.decode(
            refresh_token,
            current_app.config['REFRESH_SECRET_KEY'],
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Refresh token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid refresh token")

def generate_refresh_token(user):
    """Create new refresh token"""
    refresh_payload = {
        "user_id": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    return jwt.encode(
        refresh_payload, current_app.config["REFRESH_SECRET_KEY"], algorithm="HS256"
    )