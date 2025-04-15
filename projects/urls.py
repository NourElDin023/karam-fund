from django.urls import path, include
from . import views
from .views import ProjectDetailView

urlpatterns = [
    path('add/',views.addProject,name='add_Project'),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
