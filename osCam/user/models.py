from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.
# Using Django Built in User for Now, until we need profile

class CustomUser(AbstractUser):
     email_key = models.CharField(max_length=16, blank=True)
