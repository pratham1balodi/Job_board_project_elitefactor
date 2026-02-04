# File: job_board_project_final/users/views.py
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

class SignUpView(CreateView):
    """Main Registration View."""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Account created for {user.username}!")
        return super().form_valid(form)

# Alias to fix the ImportError you saw
JobSeekerSignUpView = SignUpView 

class ProfileView(LoginRequiredMixin, TemplateView):
    """User Profile View."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
