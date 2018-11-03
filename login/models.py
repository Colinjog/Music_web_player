from django.db import models

# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=20, default="")


class PlayedMusic(models.Model):
    music_name = models.CharField(max_length=30)
    music_id = models.CharField(max_length=10)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)


