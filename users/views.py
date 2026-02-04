# File: job_board_project_final/users/views.py
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

class JobSeekerSignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/seeker_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created! You can now log in.")
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
