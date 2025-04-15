from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from django.views.generic import DetailView
from .models import Project, projectMedia, ProjectCategory
from .forms import AddNewProject
from interactions.models import ProjectComments, ProjectRatings
from django.db.models import Avg, Count
from users.models import User
from .forms import ProjectCommentsForm, ProjectRatingsForm

# Project search view
def search_projects(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search in title, description and tags
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__tag__name__icontains=query)
        ).distinct()
        
        # Add media to each project for display
        projects_with_media = [
            {"project": proj, "media": proj.media.filter(media_type="image").first()}
            for proj in projects
        ]
    else:
        projects_with_media = []
    
    context = {
        'query': query,
        'projects': projects_with_media,
        'count': len(projects_with_media)
    }
    
    return render(request, 'search_results.html', context)

# Projects by category view
def projects_by_category(request, category_id):
    category = get_object_or_404(ProjectCategory, id=category_id)
    projects = Project.objects.filter(category=category, is_active=True, is_deleted=False)
    
    # Add media to each project for display
    projects_with_media = [
        {"project": proj, "media": proj.media.filter(media_type="image").first()}
        for proj in projects
    ]
    
    context = {
        'category': category,
        'projects': projects_with_media,
        'count': len(projects_with_media)
    }
    
    return render(request, 'category_projects.html', context)

# add New Project
@login_required
def addProject(req):
    if req.method == "POST":
        form = AddNewProject(req.POST, req.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = req.user
            if not project.campaign_end:
                project.campaign_end = project.campaign_start
            project.save()

            # Handle multiple image uploads
            images = req.FILES.getlist("images")
            if images:
                for image in images:
                    projectMedia.objects.create(
                        project=project, image=image, media_type="image"
                    )

            messages.success(req, "Project added successfully!")
            return redirect("project_detail", pk=project.id)
        else:
            messages.error(
                req, "There is an error in your data. Please check for errors."
            )
    else:
        form = AddNewProject()
    return render(req, "add_project.html", {"form": form})


# Create your views here.
class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.get_object()

        context["media"] = project.media.filter(media_type="image")

        context["total_ratings"] = project.projectratings_set.aggregate(
            total_ratings=Count("ID")
        )["total_ratings"]

        project_tags = project.tags.values_list("tag", flat=True)

        similar_projects = (
            Project.objects.filter(tags__tag__in=project_tags)
            .exclude(id=project.id)
            .distinct()
            # .annotate(avg_rating=Avg("ProjectRatings__rate"))
            # .order_by("-avg_rating")[:4]
        )
        # context["similar_projects"] = similar_projects
        context["media_similar_projects"] = [
            {"project": proj, "media": proj.media.filter(media_type="image")}
            for proj in similar_projects
        ]

        context["form1"] = ProjectCommentsForm()
        
        # Check if user is authenticated and has already rated this project
        if self.request.user.is_authenticated:
            # Get the latest user rating instead of assuming there's only one
            user_ratings = ProjectRatings.objects.filter(
                user=self.request.user,
                project=project
            ).order_by('-created_at')
            
            if user_ratings.exists():
                # Use the most recent rating
                user_rating = user_ratings.first()
                context["form2"] = ProjectRatingsForm(instance=user_rating)
                context["has_rated"] = True
            else:
                context["form2"] = ProjectRatingsForm()
                context["has_rated"] = False
        else:
            context["form2"] = ProjectRatingsForm()
            context["has_rated"] = False

        context["main_comments"] = project.projectcomments_set.filter(
            is_deleted=False, parent_comment__isnull=True
        ).order_by("-created_at")

        context["replies"] = project.projectcomments_set.filter(
            is_deleted=False, parent_comment__isnull=False
        ).order_by("-created_at")

        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()

        form1 = ProjectCommentsForm(request.POST)
        form2 = ProjectRatingsForm(request.POST)

        if form1.is_valid() and "comment_text" in request.POST:
            comment = form1.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()
            return redirect("project_detail", pk=project.pk)

        if form2.is_valid() and "rate" in request.POST:
            # Find the user's most recent rating for this project (if any)
            existing_rating = ProjectRatings.objects.filter(
                user=request.user,
                project=project
            ).order_by('-created_at').first()
            
            if existing_rating:
                # Update the most recent rating
                existing_rating.rate = form2.cleaned_data['rate']
                existing_rating.save()
            else:
                # Create a new rating if none exists
                rating = form2.save(commit=False)
                rating.user = request.user
                rating.project = project
                rating.save()
                
            return redirect("project_detail", pk=project.pk)

        context = self.get_context_data()
        context["form1"] = form1
        context["form2"] = form2
        return render(request, self.template_name, context)
    

def explore(req):
    
    projects = Project.objects.filter(is_active=True, is_deleted=False)

    return render(req,'explore.html',{'projects':projects})
    
