from django.urls import path, include
from django.urls import path
from .views import ProjectDetailView, views

urlpatterns = [
    path('add/',views.addProject,name='add_Project'),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]