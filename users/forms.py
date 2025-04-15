from django import forms
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class UserProfileEditForm(forms.ModelForm):
    """Form for editing user profile details."""
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=12, required=True)
    birthdate = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    bio = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'rows': 4})
    )
    facebook_profile = forms.URLField(required=False)
    country = forms.CharField(max_length=255, required=False)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 
            'birthdate', 'bio', 'facebook_profile', 
            'country', 'profile_picture'
        ]
    
    def clean_phone_number(self):
        """Validate Egyptian phone number format."""
        phone_number = self.cleaned_data.get('phone_number')
        
        # Validate Egyptian phone number format (01[0/1/2/5] + 8 digits)
        egyptian_phone_pattern = re.compile(r"^01[0125][0-9]{8}$")
        if not phone_number or not egyptian_phone_pattern.match(phone_number):
            raise forms.ValidationError(
                "Please enter a valid Egyptian phone number (e.g., 01012345678)."
            )
        
        return phone_number

class DeleteAccountForm(forms.Form):
    """Form for confirming account deletion."""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password",
        required=True
    )
    
    confirmation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="I understand this action cannot be undone and all my projects will be transferred to a deleted user account.",
        required=True
    )