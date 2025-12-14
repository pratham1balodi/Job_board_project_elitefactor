# File: job_board_project_final/jobs/urls.py

from django.urls import path
from .views import (
    # Public Views
    JobListView,
    JobDetailView,
    
    # Job Seeker Views
    job_apply,
    SeekerDashboardView,
    
    # Employer Views
    JobPostCreateView,
    JobUpdateView,
    job_toggle_active,
    EmployerDashboardView,
    ApplicantTrackingView,
    update_application_status,
)

urlpatterns = [
    # 1. PUBLIC/SEARCH VIEWS
    
    # Main Job Search/List Page (Accessed via /jobs/)
    path('', JobListView.as_view(), name='job_list'),
    
    # Job Detail Page (Accessed via /jobs/123/)
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    
    
    # 2. JOB SEEKER ACTIONS & DASHBOARD
    
    # Job Application Action (Accessed via /jobs/123/apply/)
    path('<int:pk>/apply/', job_apply, name='job_apply'),
    
    # Job Seeker Dashboard (Accessed via /jobs/dashboard/seeker/)
    path('dashboard/seeker/', SeekerDashboardView.as_view(), name='seeker_dashboard'), 
    
    
    # 3. EMPLOYER ACTIONS & DASHBOARD
    
    # Post New Job (Accessed via /jobs/post/)
    path('post/', JobPostCreateView.as_view(), name='job_post_create'),
    
    # Employer Dashboard (Accessed via /jobs/dashboard/employer/)
    path('dashboard/employer/', EmployerDashboardView.as_view(), name='employer_dashboard'),
    
    # Edit Job Post (Accessed via /jobs/123/edit/)
    path('<int:pk>/edit/', JobUpdateView.as_view(), name='job_update'), 
    
    # Toggle Active Status (Accessed via /jobs/123/toggle/)
    path('<int:pk>/toggle/', job_toggle_active, name='job_toggle_active'),
    
    # Applicant Tracking View (Accessed via /jobs/123/applicants/)
    path('<int:pk>/applicants/', ApplicantTrackingView.as_view(), name='applicant_tracking'),
    
    # Application Status Update (Accessed via /jobs/application/123/status/INTERVIEW/)
    path('application/<int:pk>/status/<str:status>/', update_application_status, name='update_status'),
]