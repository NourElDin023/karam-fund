from django import forms
from interactions.models import ProjectComments, ProjectRatings
from .models import Project, Tag
from django.forms import DateInput



class ProjectCommentsForm(forms.ModelForm):
    class Meta:
        model = ProjectComments
        fields = ["comment_text", "parent_comment"]
        widgets = {
            "comment_text": forms.Textarea(
                attrs={
                    "class": "form-control comment-input",
                    "rows": 3,
                    "placeholder": "Write a comment...",
                }
            ),
            "parent_comment": forms.HiddenInput(),
        }


class ProjectRatingsForm(forms.ModelForm):
    RATING_LABELS = [
        (5, " Very Good"),
        (4, " Good"),
        (3, " Average"),
        (2, " Poor"),
        (1, " Bad"),
    ]

    rate = forms.ChoiceField(
        choices=RATING_LABELS,
        widget=forms.Select(  
                attrs={
            "class": "form-control"
        })
        ,  
        label="Your Rating",
     
    )

    class Meta:
        model = ProjectRatings
        fields = ["rate"]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
    images = MultipleFileField(
        required=False,
        label="Upload Images",
        widget=MultipleFileInput(attrs={'class': 'form-control'})
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

