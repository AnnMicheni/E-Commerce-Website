from django.shortcuts import render

import jwt, datetime
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt

def login(request):
    if request.method == "POST":
        import json
        body = json.loads(request.body)
        email = body.get("email")
        password = body.get("password")
        user = authenticate(request, username=email, password=password)

        if user:
            payload = {
                "id": user.id,
                "email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                "iat": datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            refresh_payload = {
                "id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
                "iat": datetime.datetime.utcnow()
            }
            refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

            return JsonResponse({"access": token, "refresh": refresh_token})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "POST request required"}, status=400)

