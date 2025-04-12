from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import AddNewProject
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from users.models import User
# Create your views here.


@login_required
def addProject(req):
    
    

    if req.method == "POST":
        form = AddNewProject(req.POST,req.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = req.user
            if not project.campaign_end:
                project.campaign_end = project.campaign_start 
            project.save()
            
            # Handle Image uploads
            images = form.cleaned_data.get('images')
            if images:
                for image in images:
                    projectMedia.objects.create(project=project, image=image)
            
            
            
            messages.success(req,"Project added successfully!")
            return redirect('project_details',project_id=project.id)
        else:
            messages.error(req,"There is an error in your data. Please check for errors.")     
        
    
    else:
        form = AddNewProject()
    return render(req,'add_project.html',{'form':form})



def  project_details(req,project_id):
    project = get_object_or_404(Project,id=project_id)
    
    media = project.media.all()
    
    return render(req, 'project_details.html', {'project': project,'media':media})


# def addProject(req):
    
#     form = AddNewProject()
#     user = User.objects.first()
#     if req.method == "POST":
#         project = form.save(commit=False)
#         project.creator = user
#         project.save()
        
#         category = ProjectCategory.objects.create(
#             name = 
#         )
        
        
        
    
    
#     return render(req,'add_project.html',{'form':form})