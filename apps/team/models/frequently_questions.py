from django.db import models


class FrequentlyQuestions(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return str(self.id) + self.question
