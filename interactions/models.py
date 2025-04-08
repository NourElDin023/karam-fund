from django.db import models
from projects.models import Project
from users.models import User


# Create your models here.


class commonFields(models.Model):
    """common fields for models"""

    ID = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class ProjectComments(commonFields):
    """Model for project comments"""

    comment_text = models.TextField()
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    is_deleted = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)

    def report(self):
        """when the user reports the comment"""
        self.is_reported = True
        self.save()(update_fields=["is_reported"])

    def approve_report(self):
        """when the admin approves the report"""
        self.is_deleted = True
        self.save()(update_fields=["is_deleted"])

    def reject_report(self):
        """when the admin rejects the report"""
        self.is_reported = False
        self.save()(update_fields=["is_reported"])

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.title}"


class ProjectRatings(commonFields):
    """Model for project ratings"""

    rate = models.IntegerField()

    def __str__(self):
        return f"Rating by {self.user.username} on {self.project.title}"
