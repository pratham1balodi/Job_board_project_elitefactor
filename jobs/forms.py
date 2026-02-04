from django import forms
from .models import JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        # MUST MATCH THE MODEL: No 'salary_range' here!
        fields = ['title', 'category', 'description', 'location', 'salary_min', 'salary_max', 'is_active']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
        }
