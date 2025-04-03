from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class projectMedia(models.Model):
    project = models.ForeignKey('Project',related_name='media',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_media/images/',blank=True,null=True)
    video_url = models.URLField(max_length=200,blank=True,null=True)
    media_type = models.CharField(max_length=20, choices=[('image','Image'),('video','Video')])
    def __str__(self):
        return f"Media for {self.project.title} ({self.media_type})"
    
class ProjectTags(models.Model):
    project = models.ForeignKey('Project',related_name='tags',on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag',related_name='Projects',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"
    
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.name