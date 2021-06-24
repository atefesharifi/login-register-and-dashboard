from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.models.team import Team


class User(AbstractUser):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, related_name='uteam')
    file_resume = models.FileField(upload_to='media/resume/', null=True)
    code = models.FileField(upload_to='media/code/', null=True)

    def __str__(self):
        return str(self.first_name)
