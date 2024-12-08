from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    chat_id = models.BigIntegerField(blank=True, null=True)
    link_code = models.CharField(max_length=100, blank=True, null=True)
