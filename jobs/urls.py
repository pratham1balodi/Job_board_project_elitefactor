from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.JobListView.as_view(), name='job_list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    
    # Seeker
    path('seeker/dashboard/', views.SeekerDashboardView.as_view(), name='seeker_dashboard'),
    path('job/<int:pk>/apply/', views.apply_to_job, name='apply_to_job'),
    
    # Employer
    path('employer/dashboard/', views.EmployerDashboardView.as_view(), name='employer_dashboard'),
    path('employer/job/create/', views.JobCreateView.as_view(), name='job_create'),
]
