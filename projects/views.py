from django.shortcuts import render,redirect
from .models import *


# Create your views here.



def addProject(req):
    return render(req,'add_project.html')