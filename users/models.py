from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class User(AbstractUser):
    # AbstractUser already has:
    # - id, username, password, first_name, last_name, email
    # - is_active, is_staff, is_superuser, date_joined, last_login

    # Custom fields needed
    phone_number = models.CharField(max_length=12)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    # is_activated - we'll use Django's built-in is_active field
    birthdate = models.DateField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    # created_at - we'll use date_joined field

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}" if self.first_name else self.username
        )


# Create a dummy user for deleted accounts
def get_deleted_user():
    deleted_user, created = User.objects.get_or_create(
        username="deleted_user",
        defaults={
            "first_name": "Deleted",
            "last_name": "User",
            "email": "deleted@example.com",
            "is_active": False,
            "phone_number": "000000000000",
        },
    )
    return deleted_user.id


# Signal to handle user deletion
@receiver(pre_delete, sender=User)
def handle_user_deletion(sender, instance, **kwargs):
    # Skip transfer for deleted_user or admins trying to delete their account
    if instance.username == "deleted_user" or instance.is_admin:
        return

    deleted_user_id = get_deleted_user()

    # Transfer projects
    if hasattr(instance, "project_set"):
        instance.project_set.update(creator=deleted_user_id)

    # Transfer donations
    if hasattr(instance, "projectdonations_set"):
        instance.projectdonations_set.update(user=deleted_user_id)

    # Transfer comments
    if hasattr(instance, "projectcomments_set"):
        instance.projectcomments_set.update(user=deleted_user_id)

    # Transfer ratings
    if hasattr(instance, "projectrate_set"):
        instance.projectrate_set.update(user=deleted_user_id)
