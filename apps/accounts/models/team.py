from django.db import models

from common.validators import mobile_validator, mobile_length_validator, FARSI_LANGUAGE, EN_LANGUAGE


class Team(models.Model):
    fa_name = models.CharField(max_length=50, unique=True, validators=[FARSI_LANGUAGE])
    en_name = models.CharField(max_length=50, unique=True, validators=[EN_LANGUAGE])
    phone = models.CharField(null=True, max_length=11, unique=True,
                             validators=[mobile_validator, mobile_length_validator])

    def __str__(self):
        return str(self.en_name)
