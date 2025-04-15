from django.urls import path, include
from . import views
from .views import ProjectDetailView

urlpatterns = [
    path('add/',views.addProject,name='add_Project'),
    path("explore", views.explore, name="explore"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("search/", views.search_projects, name="search_projects"),
    path("category/<int:category_id>/", views.projects_by_category, name="projects_by_category"),
    path("cancel/<int:project_id>/", views.cancel_project, name="cancel_project"),
]
