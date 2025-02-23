from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.models.userModel import User
from app.libs.error_helper import handle_error
from app.libs.send_email_helper import send_email
from app.libs.otp_helper import generate_otp  # Import the generate_otp function
from datetime import datetime

otp_store = {}  # In-memory store for OTPs (use Redis or a database in production)

from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.models.userModel import User
from app.libs.error_helper import handle_error
from app.libs.send_email_helper import send_email
from app.libs.otp_helper import generate_otp
from datetime import datetime

otp_store = {}  # In-memory OTP store (consider Redis for production)

MAX_OTP_REQUESTS_PER_DAY = 3  # 🔥 Limit OTP requests per user per day

def request_password_reset():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return handle_error("Email is required", 400)

        user = User.find_user_by_email(email)
        if not user:
            return handle_error("User not found", 404)

        now = datetime.utcnow()
        last_request_time = user.get("last_request_time")
        otp_request_count = user.get("otp_request_count", 0)

        # 🔥 Check if last request was today
        if last_request_time:
            last_request_time = datetime.strptime(last_request_time, "%Y-%m-%d %H:%M:%S")
            if last_request_time.date() == now.date():
                if otp_request_count >= MAX_OTP_REQUESTS_PER_DAY:
                    return handle_error("You have reached the maximum number of OTP requests for today", 429)
            else:
                otp_request_count = 0  # 🔥 Reset count for a new day

        # Generate and send OTP
        otp = generate_otp()
        otp_store[email] = {"otp": otp, "timestamp": now}  # Store OTP with timestamp
        subject = "Password Reset OTP"
        text_content = f"Your OTP code is {otp}. It is valid for 5 minutes."
        send_email(email, subject, text_content)

        # 🔥 Update OTP request count and timestamp in DB
        User.update_user_by_id(user["_id"], {
            "otp_request_count": otp_request_count + 1,
            "last_request_time": now.strftime("%Y-%m-%d %H:%M:%S")
        })

        return jsonify({"message": "OTP sent to your email"}), 200

    except Exception as e:
        return handle_error(f"Failed to send OTP: {str(e)}", 500)

def reset_password():
    try:
        data = request.get_json()
        email = data.get("email")
        otp = data.get("otp")
        new_password = data.get("new_password")

        if not email or not otp or not new_password:
            return handle_error("Email, OTP, and new password are required", 400)

        stored_otp = otp_store.get(email)
        if not stored_otp or stored_otp != otp:
            return handle_error("Invalid or expired OTP", 400)

        user = User.find_user_by_email(email)
        if not user:
            return handle_error("User not found", 404)

        # Update the user's password
        hashed_password = generate_password_hash(new_password)
        User.update_user_by_id(user["_id"], {"password": hashed_password})

        # Send confirmation email
        subject = "Password Reset Confirmation"
        text_content = "Your password has been reset successfully."
        send_email(email, subject, text_content)

        return jsonify({"message": "Password reset successfully"}), 200

    except Exception as e:
        return handle_error(f"Failed to reset password: {str(e)}", 500)