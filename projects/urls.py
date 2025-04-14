from django.urls import path, include
from . import views
from .views import ProjectDetailView

urlpatterns = [
    path('add/',views.addProject,name='add_Project'),
    path('<int:project_id>/details/', views.project_details, name='project_details'),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
