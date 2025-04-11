from django import forms
from .models import Project, ProjectCategory, Tag, projectMedia

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'target_amount', 'category', 'campaign_end']
    
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    media_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    media_videos = forms.URLField(required=False)