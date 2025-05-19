import json
import random
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import OTPVerification
from .tokenhandler import generate_otp, send_register_otp, generate_tokens, send_reset_otp

User = get_user_model()

"""
user is created and otp sent
"""


def send_otp_email(email, otp):
    pass


@csrf_exempt
def send_register_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)
            otp = generate_otp()
            send_otp_email(email, otp)
            return JsonResponse({"message": "OTP Sent successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def verify_register_otp(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")

            if not email or not otp:
                return JsonResponse({"error": "Email and OTP are required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            otp_entry = OTPVerification.objects.filter(user=user, otp=otp).order_by('-created_at').first()

            if not otp_entry or not otp_entry.is_valid():
                return JsonResponse({"error": "Invalid or expired OTP"}, status=400)

            # Mark as verified and activate account
            user.is_otp_verified = True
            user.is_active = True
            user.save()

            otp_entry.delete()

            return JsonResponse({"message": "OTP verified. Account activated."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def create_user(request):
    """
    Register a new user and send OTP for email verification.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            #username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email, and password are required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)

            user = User.objects.create(
                #username=username,
                email=email,
                password=make_password(password),
                is_active=False  # Don't allow login until OTP is verified
            )

            otp = f"{random.randint(100000, 999999)}"
            OTPVerification.objects.create(user=user, otp=otp)

            print(f"OTP for {email} is {otp}")  # Replace with email sending logic

            return JsonResponse({"message": "User created. OTP sent to email."}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def login(request):
     if request.method == "POST":
         try:
             data = json.loads(request.body)
             email = data.get("email")
             password = data.get("password")

             user = authenticate(request, email=email, password=password)

             if user is not None:
                 tokens = generate_tokens(user)
                 print(tokens)
                 return JsonResponse({
                     "message": "Login successful",
                     "user": {
                         "id": str(user.id),
                         "email": user.email
                     },
                 }, status=200)

             return JsonResponse({"error": "Invalid credentials"}, status=401)

         except Exception as e:
             return JsonResponse({"error": str(e)}, status=400)

     return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Send the OTP via email
            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is: {otp}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({"message": "OTP sent successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def login_request_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
            send_otp(email)
            return JsonResponse({"message": "OTP sent to email"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Successfully logged out"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def send_reset_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "User does not exist"}, status=404)

            # Generate OTP
            otp = f"{random.randint(100000, 999999)}"
            send_reset_otp(email, otp)
            user.reset_otp = otp
            user.save()
            return JsonResponse({"message": "OTP sent to email"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def verify_reset_otp(request):
    """Resets the user's password after OTP verification."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            reset_otp = data.get("reset_otp")

            if not email or not reset_otp:
                return JsonResponse({"error": "Email, OTP are required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "User does not exist"}, status=404)
            if user.reset_otp != reset_otp:
                return JsonResponse({"Invalid OTP"})
            # Reset password
            user.is_otp_verified = True
            user.save()
            # Delete used OTP
            reset_otp.delete()
            return JsonResponse({"message": "OTP confirmed successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def reset_password(request):
    if request.Method != "POST":
       try:
         data = json.loads(request.body)
         new_password = data.get("new_password")
         email = data.get("email")
         if not new_password or not email:
            return JsonResponse({"error:": "New password and email cannot be blank"})
         user = User.objects.filter(email=email).first()
         if user.is_otp_verified:
            user.password = new_password
            user.is_reset_otp_verified = False
            user.save()
            return JsonResponse({"message": "Password Changed Successfully"}, status=200)
       except Exception as e:
             return JsonResponse({"error": str(e)}, status=400)



