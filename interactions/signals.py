from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import ProjectRatings
from projects.models import Project


@receiver([post_save, post_delete], sender=ProjectRatings)
def update_project_average_rating(sender, instance, **kwargs):
    project = instance.project
    avg = (
        ProjectRatings.objects.filter(project=project).aggregate(avg=Avg("rate"))["avg"]
        or 0
    )
    project.avg_rating = round(avg, 2)
    project.save()
