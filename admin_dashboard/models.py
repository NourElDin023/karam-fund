from django.db import models
from projects.models import Project

# Create your models here.

class AdminSelectedprojects(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin Selecte: {self.project.title}"
