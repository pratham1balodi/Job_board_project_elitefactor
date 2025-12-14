# File: job_board_project_final/users/urls.py

from django.urls import path
from .views import JobSeekerSignUpView, EmployerSignUpView
# Make sure both views are correctly imported

urlpatterns = [
    # Job Seeker Registration (Accessed via /accounts/signup/seeker/)
    path('signup/seeker/', JobSeekerSignUpView.as_view(), name='seeker_signup'),
    
    # Employer Registration (Accessed via /accounts/signup/employer/)
    path('signup/employer/', EmployerSignUpView.as_view(), name='employer_signup'),
    
    # Note: Login/Logout paths are handled automatically by the 'django.contrib.auth.urls' 
    # included in your core/urls.py.
]