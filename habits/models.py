from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    period_days = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration_seconds = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)
