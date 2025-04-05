from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from users.models import User
from projects.models import Project

# Create your models here.

class ProjectDonations(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    donation_date = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Donation amount must be greater than zero.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)  
        Project.objects.filter(id=self.project.id).update(current_amount=F('current_amount') + self.amount)        
        
    def __str__(self):
        user = self.user.username if self.user else 'Unknown User'
        project = self.project.title if self.project else 'Unknown Project'
        return f"{user} donated {self.amount} to {project}"