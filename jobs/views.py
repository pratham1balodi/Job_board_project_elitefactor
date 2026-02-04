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

# --- Role Check Functions (Using your Integer-based Models) ---
def is_employer(user):
    """Checks if the user has the Employer role (Integer 2)."""
    return user.is_authenticated and hasattr(user, 'role') and user.role == 2
    
def is_job_seeker(user):
    """Checks if the user has the Job Seeker role (Integer 1)."""
    return user.is_authenticated and hasattr(user, 'role') and user.role == 1


# =========================================================================
# 1. CORE & PUBLIC VIEWS
# =========================================================================

class HomepageView(TemplateView):
    """Displays the homepage with analytics. Fixed to prevent 500 errors."""
    template_name = 'homepage.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Match your model's integer roles
            context['total_jobs'] = JobPost.objects.filter(is_active=True).count()
            context['total_employers'] = User.objects.filter(role=2).count()
        except:
            context['total_jobs'] = 0
            context['total_employers'] = 0
        return context

class JobListView(ListView):
    """Displays all active jobs with search filters."""
    model = JobPost
    template_name = 'jobs/job_list.html'
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
    """Displays single job details."""
    model = JobPost
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.role == 1:
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
    """Handles job application."""
    job = get_object_or_404(JobPost, pk=pk)
    if request.user.role != 1:
        messages.error(request, "Only Job Seekers can apply.")
        return redirect('job_detail', pk=job.pk)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied.")
        return redirect('job_detail', pk=job.pk)
        
    if request.method == 'POST':
        Application.objects.create(job=job, applicant=request.user, status='APPLIED')
        messages.success(request, "Successfully applied!")
        return redirect('job_detail', pk=job.pk)

    return redirect('job_detail', pk=job.pk)

@method_decorator(user_passes_test(is_job_seeker, login_url='/accounts/login/'), name='dispatch')
class SeekerDashboardView(LoginRequiredMixin, TemplateView):
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
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        messages.success(self.request, "Job posted!")
        return super().form_valid(form)

@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html' 
    success_url = reverse_lazy('employer_dashboard')

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)

@method_decorator(user_passes_test(is_employer, login_url='/accounts/login/'), name='dispatch')
class EmployerDashboardView(LoginRequiredMixin, TemplateView):
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
def job_toggle_active(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    if job.employer != request.user:
        messages.error(request, "Access denied.")
        return redirect('employer_dashboard')
    job.is_active = not job.is_active
    job.save()
    return redirect('employer_dashboard')

@user_passes_test(is_employer, login_url='/accounts/login/')
def update_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)
    if application.job.employer != request.user:
        raise PermissionDenied
    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
    if status.upper() in valid_statuses:
        application.status = status.upper()
        application.save()
    return redirect('applicant_tracking', pk=application.job.pk)
