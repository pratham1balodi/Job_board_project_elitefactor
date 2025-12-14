# File: job_board_project_final/core/urls.py (CORRECTED CODE)

from django.contrib import admin
from django.urls import path, include
from jobs.views import HomepageView # <-- Correct import

urlpatterns = [
    # 1. ROOT PATH (The New Homepage) - MUST BE FIRST
    # This ensures the new static homepage loads when visiting http://127.0.0.1:8000/
    path('', HomepageView.as_view(), name='homepage'), 

    # 2. JOB APP URLs
    # This handles all job-related paths (e.g., /jobs/, /jobs/post/, /jobs/1/detail/)
    path('jobs/', include('jobs.urls')), 

    # 3. ACCOUNT/AUTH URLs
    # Django processes paths starting with 'accounts/'
    path('accounts/', include('django.contrib.auth.urls')), # Built-in auth (login, logout, password reset)
    path('accounts/', include('users.urls')),               # Custom user app (signup/seeker, signup/employer)

    # 4. ADMIN SITE
    path('admin/', admin.site.urls),
]