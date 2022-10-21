from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    roles = models.JSONField(default=list, null=False)

    @property
    def owner(self):
        return self
