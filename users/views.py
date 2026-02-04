from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import User

class JobSeekerSignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/seeker_signup.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
