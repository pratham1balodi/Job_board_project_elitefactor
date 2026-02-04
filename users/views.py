from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

class JobSeekerSignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    # This points to the exact file you have on GitHub
    template_name = 'users/seeker_signup.html' 
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Registration successful! Please login.")
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
