from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import DetailView
from .models import Project,projectMedia
from .forms import AddNewProject
from interactions.models import ProjectComments, ProjectRatings
from django.db.models import Avg, Count
from users.models import User
from .forms import ProjectCommentsForm, ProjectRatingsForm

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
            images = req.FILES.getlist('images')
            if images:
                for image in images:
                    projectMedia.objects.create(project=project, image=image, media_type='image')

            messages.success(req, "Project added successfully!")
            return redirect('project_details', project_id=project.id)
        else:
            messages.error(req, "There is an error in your data. Please check for errors.")
    else:
        form = AddNewProject()
    return render(req, 'add_project.html', {'form': form})


def project_details(req, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(req, 'project_details.html', {'project': project})




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
        context["form2"] = ProjectRatingsForm()

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
            rating = form2.save(commit=False)
            rating.user = request.user
            rating.project = project
            rating.save()
            return redirect("project_detail", pk=project.pk)

        context = self.get_context_data()
        context["form1"] = form1
        context["form2"] = form2
        return render(request, self.template_name, context)
