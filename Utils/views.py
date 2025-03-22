from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@login_required
def admin_dashboard(request):
    if request.user.role == "admin":
        return HttpResponse("Welcome to the Admin Dashboard!")
    else:
        return HttpResponse("Access Denied. You are not an admin.")

def assign_role(request, user_id, role):
    user = get_object_or_404(CustomUser, id=user_id)

    if role in ["admin", "manager", "staff"]:  # Ensure valid role
        user.role = role
        user.save()
        return HttpResponse(f"Role updated to {role} for user {user.username}")

    return HttpResponse("Invalid role", status=400)


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect("home")

    return render(request, "Utils/register.html")
@login_required
def user_profile(request):
    return render(request, 'Utils/profile.html')
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, "Utils/register.html", {"form": form})