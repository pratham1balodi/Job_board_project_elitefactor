from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    """
    Complete Registration Form: Fixed for your Integer-based roles (1 and 2).
    """
    class Meta(UserCreationForm.Meta):
        model = User
        # Ensure these fields match your 'models.py' exactly
        fields = UserCreationForm.Meta.fields + (
            'role', 
            'email', 
            'first_name', 
            'last_name', 
            'company_name'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to make it look like your 'bigger' version
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.label}'
            })
