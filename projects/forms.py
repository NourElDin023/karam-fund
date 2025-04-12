from django import forms
from .models import Project,Tag
class AddNewProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','target_amount','category']
        
    
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),widget=forms.CheckboxSelectMultiple, required=False)
    