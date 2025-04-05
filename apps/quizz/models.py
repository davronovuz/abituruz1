from django.db import models
from django.conf import settings

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50)  # e.g. 'single', 'multiple'
    video = models.URLField(blank=True, null=True)
    audio = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.question_text[:50]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField()


class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField()
    incorrect_answers = models.PositiveIntegerField()
    total_score = models.FloatField()
    is_passed = models.BooleanField()
    completed_at = models.DateTimeField()


class LeaderBoard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()
    rank = models.PositiveIntegerField()


class TestSetting(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField()
    max_score = models.FloatField()
    pass_percentage = models.FloatField()


class TestSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)


class BlockedTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_unblocked = models.BooleanField(default=False)
    unblocked_date = models.DateTimeField(null=True, blank=True)


class Feedback(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
