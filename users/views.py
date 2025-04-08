from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
import re


# Create your views here.
def register(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm_password").strip()
        phone_number = request.POST.get("phone_number").strip()

        # Validate data
        errors = []

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        # Password validation
        if not password:
            errors.append("Password is required.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(list(e.messages))

        # Validate Egyptian phone number format (01[0/1/2/5] + 8 digits)
        egyptian_phone_pattern = re.compile(r"^01[0125][0-9]{8}$")
        if not phone_number or not egyptian_phone_pattern.match(phone_number):
            errors.append(
                "Please enter a valid Egyptian phone number (e.g., 01012345678)."
            )

        # Check required fields
        if not all([first_name, last_name, email, password, confirm_password]):
            errors.append("All fields are required.")

        # If there are errors, show them and return to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(
                request,
                "users/register.html",
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone_number": phone_number,
                },
            )

        # Create new user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )
            messages.success(request, "Registration successful! You can now login.")
            return redirect("users:login")
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")

    # If GET request, show empty form
    return render(request, "users/register.html", {})


def login(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        
        # Basic validation
        errors = []
        
        if not email:
            errors.append("Email is required")
            
        if not password:
            errors.append("Password is required")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "users/login.html", {"email": email})
        
        # Try to authenticate the user
        # Since we're using email as username, we need to use the email as username
        user = authenticate(username=email, password=password)
        
        if user is not None:
            if user.is_active:
                # Login the user
                auth_login(request, user)
                return redirect("/")  # Redirect to homepage or dashboard
            else:
                messages.error(request, "Your account is not active. Please check your email for activation link.")
        else:
            messages.error(request, "Invalid email or password")
        
        return render(request, "users/login.html", {"email": email})
    
    # If GET request, show empty form
    return render(request, "users/login.html", {})