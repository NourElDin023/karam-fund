from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from .models import ProjectDonations
from django.utils import timezone

# Create your views here.
@login_required
def donate_to_project(request, project_id):
    project = get_object_or_404(
        Project, id=project_id, is_active=True, is_deleted=False
    )

    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Donation amount must be greater than zero.")
                return redirect("donate_to_project", project_id=project_id)

            # Create the donation
            donation = ProjectDonations.objects.create(
                user=request.user,
                project=project,
                amount=amount,
                created_at=timezone.now(),
            )

            # Update the current amount of the project
            project.current_amount += amount
            project.save()

            messages.success(
                request,
                f"Thank you for your donation of ${amount:.2f} to {project.title}!",
            )
            return redirect("project_detail", pk=project_id)

        except ValueError:
            messages.error(request, "Please enter a valid amount.")
            return redirect("donate_to_project", project_id=project_id)

    context = {"project": project}
    return render(request, "donations/donate.html", context)
