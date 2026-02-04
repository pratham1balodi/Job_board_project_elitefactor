# File: job_board_project_final/users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, ProfileView  # Use the names from your views.py

urlpatterns = [
    # Registration & Profile
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Authentication (Standard Django Views)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
]
