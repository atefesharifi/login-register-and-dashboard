from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.models.team import Team


class User(AbstractUser):
    
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, related_name='uteam')
    file_resume = models.FileField(upload_to='media/resume/', null=True)
    code = models.FileField(upload_to='media/code/', null=True)

    def __str__(self):
        return str(self.first_name)

    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """