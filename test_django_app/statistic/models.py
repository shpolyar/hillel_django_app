from django.db import models


class UserStat(models.Model):
    created = models.DateTimeField('created', auto_now_add=True)
    headers = models.TextField('headers')

    def __str__(self):
        return str(self.id)
