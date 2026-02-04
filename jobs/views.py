from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import JobPost, Application
from users.models import User
from .forms import JobPostForm

# --- Homepage ---
class HomepageView(TemplateView):
    template_name = 'homepage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['total_jobs'] = JobPost.objects.count()
            context['total_employers'] = User.objects.filter(role=2).count()
        except:
            context['total_jobs'] = 0
            context['total_employers'] = 0
        return context

# --- Job List & Detail ---
class JobListView(ListView):
    model = JobPost
    template_name = 'jobs/job_list.html'
    context_object_name = 'job_posts'
    def get_queryset(self):
        return JobPost.objects.filter(is_active=True).order_by('-created_at')

class JobDetailView(DetailView):
    model = JobPost
    template_name = 'jobs/job_detail.html'

# --- SEEKER ACTIONS (This fixes your AttributeError) ---

def apply_to_job(request, pk):
    """Handles the application logic when a user clicks 'Apply'."""
    if not request.user.is_authenticated:
        return redirect('login')
        
    job = get_object_or_404(JobPost, pk=pk)
    
    # Ensure only Job Seekers (Role 1) can apply
    if request.user.role != 1:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_detail', pk=pk)

    # Prevent double applications
    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    if already_applied:
        messages.info(request, "You have already applied for this position.")
    else:
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, "Application submitted successfully!")
        
    return redirect('seeker_dashboard')

class SeekerDashboardView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/seeker_dashboard.html'
    context_object_name = 'applications'
    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).order_by('-applied_at')

# --- EMPLOYER ACTIONS ---

class EmployerDashboardView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'jobs/employer_dashboard.html'
    context_object_name = 'jobs'
    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user).order_by('-created_at')

class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super().form_valid(form)
