# File: job_board_project_final/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# =================================================================
# 1. JOB SEEKER REGISTRATION FORM (Role: IS_JOB_SEEKER = 1)
# =================================================================
class JobSeekerCreationForm(UserCreationForm):
    """
    Form for Job Seekers. Inherits from UserCreationForm for security 
    and sets the role automatically upon save.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        # Fields required for a simple job seeker profile
        fields = ('username', 'email', 'first_name', 'last_name',)
        
    def save(self, commit=True):
        # Call the base save method to create the user with username/password
        user = super().save(commit=False)
        
        # CRITICAL: Set the role explicitly to Job Seeker
        user.role = User.IS_JOB_SEEKER
        
        if commit:
            user.save()
        return user

# =================================================================
# 2. EMPLOYER REGISTRATION FORM (Role: IS_EMPLOYER = 2)
# =================================================================
class EmployerCreationForm(UserCreationForm):
    """
    Form for Employers. Adds the required 'company_name' field 
    and sets the role automatically upon save.
    """
    # Custom Field: Required for the employer profile
    company_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Your Company Name'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Include company_name along with base fields
        fields = ('username', 'email', 'first_name', 'last_name', 'company_name',)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # CRITICAL: Set the role explicitly to Employer
        user.role = User.IS_EMPLOYER
        
        # Save the company name from the extra form field
        user.company_name = self.cleaned_data.get('company_name') 
        
        if commit:
            user.save()
        return user