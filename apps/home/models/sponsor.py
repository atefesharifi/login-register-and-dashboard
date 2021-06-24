from django.db import models


class Sponsor(models.Model):
    s_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='media\logo')
    kind = models.CharField(max_length=50)

    def __str__(self):
        return self.s_name
