import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import FileSystemStorage
from apps.team.models.team import Team
from facecup import settings

RESUME_FILE_PATH = 'files/resume/admins'


class User(AbstractUser):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, related_name='uteam')
    file_resume = models.FileField(upload_to=RESUME_FILE_PATH, null=True)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return str(self.first_name)

    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
