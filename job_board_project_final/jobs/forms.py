# File: job_board_project_final/jobs/forms.py

from django import forms
from .models import JobPost

class JobPostForm(forms.ModelForm):
    # Using ModelForm is high code quality for CRUD operations
    class Meta:
        model = JobPost
        # Fields the employer is allowed to set
        fields = [
            'title', 
            'description', 
            'location', 
            'category', 
            'salary_min', 
            'salary_max'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Applying Bootstrap 'form-control' class to all fields for UI/UX
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})