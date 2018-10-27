from django.db import models

# Create your models here.

class Played_Music(models.Model):

class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

