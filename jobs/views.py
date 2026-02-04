# File: job_board_project_final/jobs/views.py

# --- Django Imports ---
from django.views.generic import (
    ListView, CreateView, TemplateView, DetailView, UpdateView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# --- Local Imports ---
from .models import JobPost, Application
from .filters import JobFilter
from .forms import JobPostForm
from users.models import User

# --- Role Check Functions (RBAC) ---
def is_employer(user):
    """Checks if the user is authenticated and has the Employer role."""
    return user.is_authenticated and user.role == User.IS_EMPLOYER
    
def is_job_seeker(user):
    """Checks if the user is authenticated and has the Job Seeker role."""
    return user.is_authenticated and user.role == User.IS_JOB_SEEKER


# =========================================================================
# 1. CORE & PUBLIC VIEWS
# =========================================================================

# --- Static Homepage View (NEW) ---
class HomepageView(TemplateView):
    """Displays the static project homepage with basic analytics."""
    template_name = 'homepage.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass data needed for the professional homepage template
        context['total_jobs'] = JobPost.objects.filter(is_active=True).count()
        context['total_employers'] = User.objects.filter(role=User.IS_EMPLOYER).count()
        return context

# --- Job List View (For Job Seekers and Guests) ---
class JobListView(ListView):
    model = JobPost
    template_name = 'jobs/job_list.html'
    context_object_name = 'job_posts'
    paginate_by = 10 
    
    def get_queryset(self):
        # Filter for active jobs and apply search filters
        queryset = JobPost.objects.filter(is_active=True).order_by('-created_at')
        self.filterset = JobFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = JobPost.CATEGORY_CHOICES
        return context

# --- Job Detail View ---
class JobDetailView(DetailView):
    model = JobPost
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.role == User.IS_JOB_SEEKER:
            # Check if the seeker has already applied to this job (for UX)
            context['has_applied'] = Application.objects.filter(
                job=self.object, 
                applicant=self.request.user
            ).exists()
        return context


# =========================================================================
# 2. JOB SEEKER VIEWS & ACTIONS
# =========================================================================

# --- Job Application View (FBV) ---
@login_required(login_url='/accounts/login/')
def job_apply(request, pk):
    """Handles the application process for a Job Seeker."""
    job = get_object_or_404(JobPost, pk=pk)
    
    # 1. Role Check: Ensure only Job Seekers can apply
    if request.user.role != User.IS_JOB_SEEKER:
        messages.error(request, "Only Job Seekers can apply for jobs.")
        return redirect('job_detail', pk=job.pk)

    # 2. Check if already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, f"You have already applied for '{job.title}'.")
        return redirect('job_detail', pk=job.pk)
        
    # 3. Create Application (Requires POST request from the job_detail button)
    if request.method == 'POST':
        Application.objects.create(job=job, applicant=request.user, status='APPLIED')
        messages.success(request, f"Successfully applied for '{job.title}'!")
        return redirect('job_detail', pk=job.pk)

    return redirect('job_detail', pk=job.pk)

# --- Job Seeker Dashboard View ---
@method_decorator(user_passes_test(is_job_seeker, login_url='/accounts/login/'), name='dispatch')
class SeekerDashboardView(LoginRequiredMixin, TemplateView):
    """Displays a list of all applications submitted by the seeker and their status."""
    template_name = 'jobs/seeker_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all applications submitted by the current user
        context['applications'] = Application.objects.filter(applicant=self.request.user).order_by('-applied_at')
        return context


# =========================================================================
# 3. EMPLOYER VIEWS & ACTIONS
# =========================================================================

# --- Job Post Creation View (Requires Employer Role) ---
@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class JobPostCreateView(CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        # Assign the currently logged-in employer to the post
        form.instance.employer = self.request.user
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)

# --- Job Update View (Requires Employer Role & Ownership) ---
@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class JobUpdateView(LoginRequiredMixin, UpdateView):
    """Allows an employer to edit their job posting."""
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html' 
    success_url = reverse_lazy('employer_dashboard')

    def get_queryset(self):
        # SECURITY CHECK: Only allow the jobs owned by the current logged-in user
        return JobPost.objects.filter(employer=self.request.user)
        
    def form_valid(self, form):
        messages.success(self.request, f"Job '{form.instance.title}' updated successfully.")
        return super().form_valid(form)

# --- Job Activation/Deactivation Toggle (FBV) ---
@user_passes_test(is_employer, login_url='/accounts/login/')
def job_toggle_active(request, pk):
    """Toggles the active status of a job post."""
    job = get_object_or_404(JobPost, pk=pk)
    
    # SECURITY CHECK: Only allow the owner to toggle status
    if job.employer != request.user:
        messages.error(request, "Permission denied: You do not own this job listing.")
        return redirect('employer_dashboard')
        
    job.is_active = not job.is_active
    job.save()
    
    status_text = "Active" if job.is_active else "Deactivated (Archived)"
    messages.success(request, f"Job '{job.title}' status changed to {status_text}.")
    
    return redirect('employer_dashboard')


# --- Employer Dashboard View ---
@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class EmployerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/employer_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        posted_jobs = JobPost.objects.filter(employer=self.request.user).order_by('-created_at')
        
        # Analytics for the dashboard cards
        total_jobs = posted_jobs.count()
        active_jobs = posted_jobs.filter(is_active=True).count()
        # Calculate total applications across all jobs
        total_applications = sum(job.applications.count() for job in posted_jobs)
        
        context['posted_jobs'] = posted_jobs
        context['total_jobs'] = total_jobs
        context['active_jobs'] = active_jobs
        context['total_applications'] = total_applications
        
        return context

# --- Applicant Tracking View (ATS) ---
@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class ApplicantTrackingView(DetailView):
    """Allows employer to view all applications for a specific job post."""
    model = JobPost
    template_name = 'jobs/applicant_tracking.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        # SECURITY CHECK: Only allow the employer who created the job to see applications
        return JobPost.objects.filter(employer=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all applications for this job
        context['applications'] = context['job'].applications.all().order_by('-applied_at')
        context['status_choices'] = Application.STATUS_CHOICES
        return context

# --- Application Status Update View (FBV) ---
@user_passes_test(is_employer, login_url='/accounts/login/')
def update_application_status(request, pk, status):
    """Allows an employer to update the status of a specific application."""
    application = get_object_or_404(Application, pk=pk)
    
    # 1. Security Check: Ensure the logged-in user owns the job post
    if application.job.employer != request.user:
        messages.error(request, "Permission denied: You do not own this job listing.")
        raise PermissionDenied
    
    # 2. Status Validation
    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
    if status.upper() not in valid_statuses:
        messages.error(request, f"Invalid status: {status}")
        return redirect('applicant_tracking', pk=application.job.pk)
        
    # 3. Update Status
    application.status = status.upper()
    application.save()
    
    messages.success(request, f"Status for {application.applicant.username} updated to {application.get_status_display()}.")
    
    # Redirect back to the tracking page for that job
    return redirect('applicant_tracking', pk=application.job.pk)
