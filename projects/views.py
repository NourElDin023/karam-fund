from django.shortcuts import render,redirect
from .models import *
from .forms import AddNewProject

# Create your views here.



def addProject(req):
    
    form = AddNewProject()
    
    
    
    return render(req,'add_project.html',{'form':form})