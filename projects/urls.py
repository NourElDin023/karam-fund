from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.addProject,name='add_Project')
]