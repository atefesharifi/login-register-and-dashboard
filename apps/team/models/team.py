from django.db import models
from common.validators import mobile_validator, mobile_length_validator, FARSI_LANGUAGE, EN_LANGUAGE

CODE_PATH = 'files/resume/codes'


class Team(models.Model):
    en_name = models.CharField(max_length=50, unique=True, validators=[EN_LANGUAGE])
    fa_name = models.CharField(max_length=50, unique=True, validators=[FARSI_LANGUAGE])
    phone = models.CharField(null=True, max_length=11, unique=True,
                             validators=[mobile_validator, mobile_length_validator])
    code = models.FileField(upload_to=CODE_PATH, null=True)

    verify_phone = models.BooleanField(default=False)

    class Meta:
        db_table = "Team"

    def __str__(self):
        return str(self.en_name)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('accounts:team', args=[self.id])
