from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    IS_JOB_SEEKER = 1
    IS_EMPLOYER = 2
    ROLE_CHOICES = ((IS_JOB_SEEKER, 'Job Seeker'), (IS_EMPLOYER, 'Employer'))
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=IS_JOB_SEEKER)
    company_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
