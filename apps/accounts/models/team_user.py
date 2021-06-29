from django.db import models

from apps.accounts.models.team import Team
from common.validators import FARSI_LANGUAGE


class TeamUser(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='mteam')
    first_name = models.CharField(max_length=100, validators=[FARSI_LANGUAGE])
    last_name = models.CharField(max_length=100, validators=[FARSI_LANGUAGE])
    file_resume = models.FileField(upload_to='media/resume')

    class Meta:
        unique_together = [['team', 'first_name', 'last_name']]

    def __str__(self):
        return str(self.first_name)
