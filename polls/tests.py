from django.test import TestCase
import datetime

from django.utils import timezone

from .models import Choice, Question
# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_futrue_question(self):
        time = timezone.now() + datetime.timedelta(days=30)

        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_rencetly(), False)
