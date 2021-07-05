from django.db import models
from datetime import datetime
from common_app.models import Account
from django.utils.timezone import now
import datetime

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('complete', 'complete'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,blank=True,related_name='task_account')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    task_date = models.DateField(default=datetime.date.today())
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Task"