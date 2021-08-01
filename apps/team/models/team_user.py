from django.db import models

from apps.team.models.team import Team
from common.validators import FARSI_LANGUAGE

RESUME_FILE_PATH = 'files/resume/team_user'


class TeamUser(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='mteam')
    first_name = models.CharField(max_length=100, validators=[FARSI_LANGUAGE])
    last_name = models.CharField(max_length=100, validators=[FARSI_LANGUAGE])
    file_resume = models.FileField(upload_to=RESUME_FILE_PATH)

    class Meta:
        db_table = "TeamUser"
        unique_together = [['team', 'first_name', 'last_name']]

    def __str__(self):
        return str(self.first_name)
