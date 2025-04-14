from django.urls import path
from . import views

urlpatterns = [
    path("<int:project_id>/", views.donate_to_project, name="donate_to_project"),
]
