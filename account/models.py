from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    # sets = models.
