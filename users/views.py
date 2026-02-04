# File: job_board_project_final/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

# Local imports from your users app
from .forms import UserRegistrationForm
from .models import User

class SignUpView(CreateView):
    """Handles new user registration with role selection."""
    model = User
    form_class = UserRegistrationForm
    # Path updated to point to your 'users' subfolder
    template_name = 'users/signup.html' 
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Account created for {user.username}! You can now log in.")
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, TemplateView):
    """Displays user profile and redirects to appropriate dashboard."""
    # Path updated to point to your 'users' subfolder
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the user object to the template
        context['user'] = self.request.user
        return context
