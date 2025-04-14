from django import forms
from interactions.models import ProjectComments, ProjectRatings


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
        widget=forms.Select,  # أو forms.Select() لو عايز Dropdown
        label="Your Rating",
    )

    class Meta:
        model = ProjectRatings
        fields = ["rate"]
