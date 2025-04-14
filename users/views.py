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
import re
from django.views.generic import DetailView



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
        
        # Try to authenticate the user
        # Since we're using email as username, we need to use the email as username
        user = authenticate(username=email, password=password)
        # TODO :Need To Be Checked as it shows "Invalid email or password" if account is not active
        if user is not None:
            if user.is_active:
                # Login the user
                auth_login(request, user)
                return redirect("/")  # Redirect to homepage or dashboard
            else:
                messages.error(request, "Your account is not active. Please check your email for activation link.")
                # Resend activation email option
                resend = request.POST.get("resend_activation")
                if resend:
                    send_activation_email(user, request)
                    messages.info(request, "Activation email has been resent.")
        else:
            messages.error(request, "Invalid email or password")
        
        return render(request, "users/login.html", {"email": email})
    
    # If GET request, show empty form
    return render(request, "users/login.html", {})

def logout(request):
    # Handle both POST and GET requests
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("users:login")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user


def profile_view(request):
    profile_user = request.user
    profile_data = getattr(profile_user, 'userprofile', None)
    
    context = {
        'profile_user': profile_user,
        'profile_data': profile_data,
        'member_since': profile_user.date_joined.strftime("%B %d, %Y")
    }
    return render(request, 'users/profile_detail.html', context)