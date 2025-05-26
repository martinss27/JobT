from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser #import used to deal with users, without it i couldn't use uuid
#Django does not allow you to customize the default user model directly.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('pending', 'Pending'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('offer', 'Offer Received'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    user_job_id = models.PositiveBigIntegerField()
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'user_job_id')
