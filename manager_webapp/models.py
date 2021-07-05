from django.db import models
from common_app.models import Account
from client_webapp.models import Task

# Create your models here.

class AssignTask(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,blank=True,related_name='assigntask_account')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='assigntask_task')
    