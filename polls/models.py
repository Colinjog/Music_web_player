from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_rencetly(self):
        return timezone.now()+datetime.timedelta(days=1) >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_rencetly.admin_order_field = 'pub_date'
    was_published_rencetly.boolean = True
    was_published_rencetly.short_description = "Published recently?"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
