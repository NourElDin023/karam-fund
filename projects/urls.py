from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.addProject,name='add_Project'),
    path('<int:project_id>/details/', views.project_details, name='project_details')
]