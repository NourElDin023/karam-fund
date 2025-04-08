from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from projects.models import Project
from interactions.models import ProjectComments
from users.models import User


class CommonFields(models.Model):
    """common fields for models"""

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    status_pending = "pending"
    status_reviewed = "reviewed"
    status_accepted = "accepted"
    status_rejected = "rejected"

    STATUS_CHOICES = [
        (status_pending, "Pending"),
        (status_reviewed, "Reviewed"),
        (status_accepted, "Accepted"),
        (status_rejected, "Rejected"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def accept(self):
        """Accept the report and mark related project as deleted"""
        self.status = self.status_accepted
        self.save(update_fields=["status"])

        # Mark the project as deleted

    def reject(self):
        """Reject the report without affecting the project"""
        self.status = self.status_rejected
        self.save(update_fields=["status"])

    def mark_as_reviewed(self):
        """Mark report as reviewed without final decision"""
        self.status = self.status_reviewed
        self.save(update_fields=["status"])

    def pending(self):
        self.status = self.status_pending
        self.save(update_fields=["status"])

    class Meta:
        abstract = True


class ProjectReport(CommonFields):
    REASON_CHOICES = [
        ("scam", "Scam"),
        ("misleading", "Misleading Information"),
        ("offensive", "Offensive Content"),
        ("other", "Other"),
    ]

    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report #{self.id} for Project {self.project}"


class CommentReport(CommonFields):
    REASON_CHOICES = [
        ("spam", "Spam"),
        ("harassment", "Harassment"),
        ("inappropriate", "inappropriate Content"),
        ("other", "Other"),
    ]
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    comment = models.ForeignKey(ProjectComments, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report #{self.id} for Comment {self.comment}"
