from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
 
class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    one_time_token = models.CharField(max_length=255, blank=True, null=True)