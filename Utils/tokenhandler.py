import datetime
import random

import jwt
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache  # To store OTP temporarily
from django.http import JsonResponse

User = get_user_model()


def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_register_otp(email,otp):
    """Generate OTP, store it in cache, and send via email"""

    # Store OTP in cache for 5 minutes
    cache.set(f"otp_{email}", otp, timeout=300)

    subject = "Your Register OTP"
    message = f"Your OTP for register is: {otp}\nThis OTP is valid for 5 minutes."

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return otp

def generate_tokens(user):
    try:
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            "iat": datetime.datetime.utcnow()
        }
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        refresh_payload = {
            "user_id": str(user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

        return {
            "access": access_token,
            "refresh": refresh_token
        }
    except Exception as e:
        # Instead of returning JsonResponse, raise the error or return a plain dict
        return {"error": f"Error in generating token: {str(e)}"}

def send_reset_otp(email,otp):
    """Generate OTP, store it in cache, and send via email"""

    subject = "Your Reset Password OTP"
    message = f"Your OTP for reset password OTP is: {otp}\nThis OTP is valid for 5 minutes."

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return otp


