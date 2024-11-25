from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    username = None

    email = models.EmailField(unique=True, blank=False)
    nickname = models.CharField(max_length=16, unique=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname
