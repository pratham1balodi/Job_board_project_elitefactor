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

class HomepageView(TemplateView):
    """Displays the static project homepage."""
    template_name = 'homepage.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jobs'] = JobPost.objects.filter(is_active=True).count()
        context['total_employers'] = User.objects.filter(role=User.IS_EMPLOYER).count()
        return context

class JobListView(ListView):
    """Displays all active jobs with search filters."""
    model = JobPost
    template_name = 'jobs/job_list.html'  # Path updated for jobs subfolder
    context_object_name = 'job_posts'
    paginate_by = 10 
    
    def get_queryset(self):
        queryset = JobPost.objects.filter(is_active=True).order_by('-created_at')
        self.filterset = JobFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = JobPost.CATEGORY_CHOICES
        return context

class JobDetailView(DetailView):
    """Displays details for a single job post."""
    model = JobPost
    template_name = 'jobs/job_detail.html' # Path updated for jobs subfolder
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.role == User.IS_JOB_SEEKER:
            context['has_applied'] = Application.objects.filter(
                job=self.object, 
                applicant=self.request.user
            ).exists()
        return context


# =========================================================================
# 2. JOB SEEKER VIEWS & ACTIONS
# =========================================================================

@login_required(login_url='/accounts/login/')
def job_apply(request, pk):
    """Handles the application process for a Job Seeker."""
    job = get_object_or_404(JobPost, pk=pk)
    
    if request.user.role != User.IS_JOB_SEEKER:
        messages.error(request, "Only Job Seekers can apply for jobs.")
        return redirect('job_detail', pk=job.pk)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, f"You have already applied for '{job.title}'.")
        return redirect('job_detail', pk=job.pk)
        
    if request.method == 'POST':
        Application.objects.create(job=job, applicant=request.user, status='APPLIED')
        messages.success(request, f"Successfully applied for '{job.title}'!")
        return redirect('job_detail', pk=job.pk)

    return redirect('job_detail', pk=job.pk)

@method_decorator(user_passes_test(is_job_seeker, login_url='/accounts/login/'), name='dispatch')
class SeekerDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard showing all applications submitted by the seeker."""
    template_name = 'jobs/seeker_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(applicant=self.request.user).order_by('-applied_at')
        return context


# =========================================================================
# 3. EMPLOYER VIEWS & ACTIONS
# =========================================================================

@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class JobPostCreateView(CreateView):
    """Allows employers to post new jobs."""
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class JobUpdateView(LoginRequiredMixin, UpdateView):
    """Allows an employer to edit their job posting."""
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html' 
    success_url = reverse_lazy('employer_dashboard')

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)
        
    def form_valid(self, form):
        messages.success(self.request, f"Job '{form.instance.title}' updated successfully.")
        return super().form_valid(form)

@user_passes_test(is_employer, login_url='/accounts/login/')
def job_toggle_active(request, pk):
    """Toggles the active status of a job post."""
    job = get_object_or_404(JobPost, pk=pk)
    
    if job.employer != request.user:
        messages.error(request, "Permission denied: You do not own this job listing.")
        return redirect('employer_dashboard')
        
    job.is_active = not job.is_active
    job.save()
    
    status_text = "Active" if job.is_active else "Deactivated (Archived)"
    messages.success(request, f"Job '{job.title}' status changed to {status_text}.")
    return redirect('employer_dashboard')

@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class EmployerDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard showing employer metrics and posted jobs."""
    template_name = 'jobs/employer_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posted_jobs = JobPost.objects.filter(employer=self.request.user).order_by('-created_at')
        
        context['posted_jobs'] = posted_jobs
        context['total_jobs'] = posted_jobs.count()
        context['active_jobs'] = posted_jobs.filter(is_active=True).count()
        context['total_applications'] = sum(job.applications.count() for job in posted_jobs)
        return context

@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class ApplicantTrackingView(DetailView):
    """Allows employer to view applications for a specific job."""
    model = JobPost
    template_name = 'jobs/applicant_tracking.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = context['job'].applications.all().order_by('-applied_at')
        context['status_choices'] = Application.STATUS_CHOICES
        return context

@user_passes_test(is_employer, login_url='/accounts/login/')
def update_application_status(request, pk, status):
    """Allows employer to update application status (APPLIED, REJECTED, etc)."""
    application = get_object_or_404(Application, pk=pk)
    
    if application.job.employer != request.user:
        messages.error(request, "Permission denied.")
        raise PermissionDenied
    
    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
    if status.upper() in valid_statuses:
        application.status = status.upper()
        application.save()
        messages.success(request, f"Status updated for {application.applicant.username}.")
    
    return redirect('applicant_tracking', pk=application.job.pk)
