from django.db import models


class Rules(models.Model):
    file = models.FileField(upload_to='media/Rules', null=True)
