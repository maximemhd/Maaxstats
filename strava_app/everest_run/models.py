# coding: utf-8
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)  # La liaison OneToOne vers le modèle User
    user_token = models.CharField(max_length=100)
    #inscrit_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

    def token(self):
        return self.token
