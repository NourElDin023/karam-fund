from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from .models import ProjectDonations
from django.utils import timezone
from decimal import Decimal, ROUND_DOWN
from django.http import Http404


# Create your views here.
@login_required
def donate_to_project(request, project_id):
    # First, try to get the project regardless of its status
    try:
        # Try to get the project without any filters first
        project = Project.objects.get(id=project_id)
        
        # Check if the project is inactive or deleted
        if not project.is_active or project.is_deleted:
            context = {
                "project": project,
                "inactive": True,
                "reason": "closed" if not project.is_active else "deleted"
            }
            return render(request, "donations/donate_inactive.html", context)
            
        # If we get here, project is active and not deleted
        donation_success = False
        donation_amount = None
        
        if request.method == "POST":
            amount = request.POST.get("amount")
            anonymous = request.POST.get("anonymous") == "on"  # Check if anonymous checkbox is checked

            try:
                # Convert to float first for validation
                amount_float = float(amount)
                if amount_float <= 0:
                    messages.error(request, "Donation amount must be greater than zero.")
                    return redirect("donate_to_project", project_id=project_id)
                
                # Round to 2 decimal places to prevent validation error
                amount_decimal = Decimal(amount_float).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
                
                # Create the donation
                donation = ProjectDonations.objects.create(
                    user=request.user,
                    project=project,
                    amount=amount_decimal,
                    anonymous=anonymous,
                )

                # Update the current amount of the project
                project.current_amount += amount_decimal
                project.save()

                # Set success flags for template
                donation_success = True
                donation_amount = amount_decimal
                
                message_type = "anonymous " if anonymous else ""
                messages.success(
                    request,
                    f"Thank you for your {message_type}donation of ${amount_decimal:.2f} to {project.title}!",
                )
                
                # Instead of redirecting, render the same page with success context
                context = {
                    "project": project,
                    "donation_success": donation_success,
                    "donation_amount": donation_amount,
                    "anonymous": anonymous
                }
                return render(request, "donations/donate_success.html", context)
                
            except ValueError:
                messages.error(request, "Please enter a valid amount.")
                return redirect("donate_to_project", project_id=project_id)

        context = {"project": project}
        return render(request, "donations/donate.html", context)
        
    except Project.DoesNotExist:
        messages.error(request, "The project you're looking for doesn't exist.")
        return redirect("home")
