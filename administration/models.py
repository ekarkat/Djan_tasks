from django.db import models
from django.contrib.auth.models import User

from core.models import BaseModel

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
        return self.user.username
