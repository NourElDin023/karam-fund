from django import forms
from .models import Project, Tag
from django.forms import DateInput

class AddNewProject(forms.ModelForm):
    """
    Form for adding a new project with fields for title, description, target amount,
    category, campaign end date, tags, and optional images.
    """
    # Tags field with multiple selection using checkboxes
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Tags"
    )

    # Campaign end date field with a date picker widget
    campaign_end = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label="Campaign End Date"
    )

    # Images field for uploading multiple images
    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        label="Upload Images"
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'target_amount', 'category', 'campaign_end']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter project description'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter target amount'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Project Title',
            'description': 'Project Description',
            'target_amount': 'Target Amount ($)',
            'category': 'Category',
        }

