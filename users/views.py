# File: job_board_project_final/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    """Form for creating a new user with a specific role."""
    
    class Meta(UserCreationForm.Meta):
        model = User
        # Ensure 'role' is included so users can choose Seeker or Employer
        fields = UserCreationForm.Meta.fields + ('role', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding Bootstrap classes for better UI
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
