# File: job_board_project_final/users/views.py
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

class JobSeekerSignUpView(CreateView):
    """Registration View using your existing seeker_signup.html template."""
    model = User
    form_class = UserRegistrationForm
    # FIX: Pointing specifically to the file you have on GitHub
    template_name = 'users/seeker_signup.html' 
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Account created for {user.username}!")
        return super().form_valid(form)

# Alias to ensure other parts of the app don't crash
SignUpView = JobSeekerSignUpView 

class ProfileView(LoginRequiredMixin, TemplateView):
    """User Profile View."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
