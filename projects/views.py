from django.shortcuts import render
from django.views.generic import DetailView
from .models import Project
from interactions.models import ProjectComments, ProjectRatings
from django.db.models import Avg, Count


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
        )
        project_tags = project.tags.values_list("tag", flat=True)

        similar_projects = (
            Project.objects.filter(tags__tag__in=project_tags).exclude(id=project.id)
            # .annotate(avg_rating=Avg("ProjectRatings__rate"))
            # .order_by("-avg_rating")[:4]
        )
        # context["similar_projects"] = similar_projects
        context["media_similar_projects"] = [
            {"project": proj, "media": proj.media.filter(media_type="image")}
            for proj in similar_projects
        ]

        return context
