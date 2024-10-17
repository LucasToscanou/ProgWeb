from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class QuestionList(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    shareable_link = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    form_link = models.URLField(blank=True, null=True)  # New field for form link

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = [
        ('title', 'Title'),
        ('multiple_choice', 'Multiple Choice'),
        ('long_answer', 'Long Answer'),
    ]
    
    question_list = models.ForeignKey(QuestionList, related_name='questions', on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=200, default='')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    multiple_choice_options = models.JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    multiple_choice_answer = models.CharField(max_length=100, blank=True, null=True)
    long_answer_answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Answer to '{self.question.text}'"
