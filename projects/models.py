from django.db import models
from django.conf import settings

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class projectMedia(models.Model):
    project = models.ForeignKey(
        "Project", related_name="media", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="project_media/images/", blank=True, null=True)
    video_url = models.URLField(max_length=200, blank=True, null=True)
    media_type = models.CharField(
        max_length=20, choices=[("image", "Image"), ("video", "Video")]
    )

    def __str__(self):
        return f"Media for {self.project.title} ({self.media_type})"


class ProjectTags(models.Model):
    project = models.ForeignKey(
        "Project", related_name="tags", on_delete=models.CASCADE
    )
    tag = models.ForeignKey("Tag", related_name="Projects", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign_start = models.DateTimeField(auto_now_add=True)
    campaign_end = models.DateField()
    is_active = models.BooleanField(default=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_reported = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def cancel_project(self):
        if self.current_amount < (0.25 * self.target_amount):
            self.is_cancelled = True
            self.save()

    def check_project_status(self):
        from django.utils.timezone import now

        if now().date() > self.campaign_end or self.is_cancelled:
            self.is_active = False
            self.save()

    @property
    def avg_rating_label(self):
        if self.avg_rating >= 4.5:
            return "Very Good"
        elif self.avg_rating >= 3.5:
            return "Good"
        elif self.avg_rating >= 2.5:
            return "Average"
        elif self.avg_rating >= 1.5:
            return "Poor"
        else:
            return "Bad"
