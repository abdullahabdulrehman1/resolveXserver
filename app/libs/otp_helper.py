import pyotp

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=1000)  # OTP valid for 5 minutes
    return totp.now()