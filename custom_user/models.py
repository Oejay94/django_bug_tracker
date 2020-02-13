from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    homepage = models.URLField(null=True)
    display_name = models.CharField(null=True, max_length=20)
    age = models.IntegerField(null=True, blank=True)

    REQUIRED_FIELDS = ['age']
