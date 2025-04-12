from django import forms
from .models import Project,Tag
from django.forms import DateInput

class AddNewProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','target_amount','category','campaign_end']
        
    
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),widget=forms.CheckboxSelectMultiple, required=False)
    campaign_end = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        required=True  # تأكد من أن الحقل مطلوب
    )