# File: job_board_project_final/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import JobSeekerCreationForm, EmployerCreationForm 
from .models import User

# --- 1. Job Seeker Sign Up View ---
class JobSeekerSignUpView(CreateView):
    """Handles registration for users with the Job Seeker role."""
    model = User
    form_class = JobSeekerCreationForm
    template_name = 'users/seeker_signup.html'
    
    # Redirect to the job list after successful registration and login
    success_url = reverse_lazy('job_list') 

    def form_valid(self, form):
        # Calls the form's save method, which sets the role (IS_JOB_SEEKER)
        valid = super().form_valid(form)
        # Log the user in immediately after successful registration
        login(self.request, self.object)
        return valid

# --- 2. Employer Sign Up View ---
class EmployerSignUpView(CreateView):
    """Handles registration for users with the Employer role."""
    model = User
    form_class = EmployerCreationForm 
    template_name = 'users/employer_signup.html'
    
    # Redirect to the job list after successful registration and login
    success_url = reverse_lazy('job_list') 

    def form_valid(self, form):
        # Calls the form's save method, which sets the role (IS_EMPLOYER) and company name
        valid = super().form_valid(form)
        # Log the user in immediately after successful registration
        login(self.request, self.object)
        return valid