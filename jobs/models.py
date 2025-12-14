# File: job_board_project_final/jobs/models.py

from django.db import models
from users.models import User 

class JobPost(models.Model):
    # Foreign Key to the Employer User (Role = 2)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    
    # Enhanced Fields for Search and Analytics
    salary_min = models.IntegerField(default=0) # Must be default 0 for range search
    salary_max = models.IntegerField(default=0)
    
    CATEGORY_CHOICES = [
        ('IT', 'Information Technology'), 
        ('HR', 'Human Resources'), 
        ('FIN', 'Finance'),
        ('MKT', 'Marketing'),
        ('SAL', 'Sales'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_jobs')
    
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('REVIEW', 'Under Review'),
        ('INTERVIEW', 'Interview Scheduled'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')
        
    def __str__(self):
        return f"Application by {self.applicant.username} for {self.job.title}"