# File: job_board_project_final/jobs/filters.py

import django_filters
from django.forms import TextInput
from .models import JobPost

class JobFilter(django_filters.FilterSet):
    # Text search across multiple fields
    search_query = django_filters.CharFilter(
        method='filter_search',
        label='Title/Description/Location',
        # Use Bootstrap form control class
        widget=TextInput(attrs={'placeholder': 'Search keywords...'}) 
    )
    
    # Filtering by Company (Employer) Name
    company = django_filters.CharFilter(
        field_name='employer__company_name', 
        lookup_expr='icontains', 
        label='Company'
    )
    
    # Salary Range Filtering (Search jobs where the MIN salary is AT LEAST the input value)
    salary_min = django_filters.NumberFilter(
        field_name='salary_min', 
        lookup_expr='gte', 
        label='Min Salary (K)'
    )

    class Meta:
        model = JobPost
        # We only define fields that use the standard exact/choice filters
        fields = ['category'] 
        
    # Custom method to search across Title, Description, and Location
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        
        # Q objects allow OR lookups (Title OR Description OR Location)
        from django.db.models import Q 
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) | 
            Q(location__icontains=value)
        )