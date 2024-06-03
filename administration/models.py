from django.db import models
from django.contrib.auth.models import User

from core.models import BaseModel
from taskmanager.models import Task, TaskRequest

# Create your models here.

class UserProfile(BaseModel):
    # user profile class with user, email, first_name, last_name, phone, image fields
    # user profile is connected to user model with one to one relationship

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        out = f"id :{self.id} - {self.user.username}"
        return out

    def address_to(self, task, user):
        # address a task to a user
        if User.objects.filter(id=user.id).exists() and self.user.id == task.owner.id:
            if user.created_tasks.filter(id=task.id).exists():
                task_request = TaskRequest.objects.create(task=task, owner=self.user, from_user=user)
                return task_request
        return None

