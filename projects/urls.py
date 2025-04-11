from django.urls import path, include

from .views import ProjectDetailView

urlpatterns = [
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
