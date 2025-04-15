from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    authenticate, 
    login as auth_login, 
    logout as auth_logout,
    get_user_model
)

User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import models  # Added missing import for database aggregation functions
import re
from django.views.generic import DetailView
from .forms import UserProfileEditForm



class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Karam Fund Account'
    email_body = render_to_string('users/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    email = EmailMessage(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,  # Changed from EMAIL_FROM_ADDRESS to EMAIL_HOST_USER
        [user.email]
    )
    email.content_subtype = "html"
    EmailThread(email).start()


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now login.")
        return redirect('users:login')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('users:login')


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
        profile_picture = request.FILES.get("profile_picture")

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
                is_active=False,  # Set user as inactive until email verification
            )
            
            # Add profile picture if provided
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()

            # Send activation email
            send_activation_email(user, request)
            
            messages.success(request, "Registration successful! Please check your email to activate your account.")
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
        
        # Try to find the user by email first
        try:
            user = User.objects.get(email=email)

            # Check if the password is correct
            if user.check_password(password):
                # Check if the user account is active
                if user.is_active:
                    # Login the user
                    auth_login(request, user)
                    # Redirect to homepage or dashboard after successful login
                    # Check if there's a 'next' parameter in the URL
                    next_url = request.GET.get("next")
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect("/")  # Default redirect to homepage
                else:
                    # User exists but account is not active
                    send_activation_email(user, request)
                    messages.warning(
                        request,
                        "Your email is not activated. We've resent the activation email, please check your inbox.",
                    )
            else:
                # Password is incorrect
                messages.error(request, "Invalid email or password")

        except User.DoesNotExist:
            # User with this email does not exist
            messages.error(request, "Invalid email or password")

        # If login fails (inactive account, wrong password, user not found), render login page again
        return render(request, "users/login.html", {"email": email})
    # If GET request, show empty form
    return render(request, "users/login.html", {})

def logout(request):
    # Handle both POST and GET requests
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("users:login")

@login_required
def profile_view(request):
    profile_user = request.user
    user_profile = getattr(profile_user, 'userprofile', None)
    
    # Get user's projects
    user_projects = profile_user.project_set.all().order_by('-campaign_start')
    
    # Add media to each project
    projects_with_media = [
        {"project": project, "media": project.media.filter(media_type="image").first()}
        for project in user_projects
    ]
    
    # Get user's donations
    from donations.models import ProjectDonations
    user_donations = ProjectDonations.objects.filter(user=profile_user).order_by('-donation_date')
    
    # Calculate total donation amount
    total_donation_amount = user_donations.aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'member_since': profile_user.date_joined.strftime("%B %d, %Y"),
        'user_projects': projects_with_media,
        'project_count': user_projects.count(),
        'user_donations': user_donations,
        'donation_count': user_donations.count(),
        'total_donation_amount': total_donation_amount
    }
    return render(request, 'users/profile_detail.html', context)

@login_required
def edit_profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Save form data
            profile = form.save(commit=False)
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            # Save the user profile
            profile.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        # Initialize the form with the current user's data
        form = UserProfileEditForm(instance=user)
    
    return render(request, 'users/edit_profile.html', {'form': form})