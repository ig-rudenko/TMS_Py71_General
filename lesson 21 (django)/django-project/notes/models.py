from django.db import models
from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


class Note(models.Model):

    user = models.ForeignKey(USER_MODEL, on_delete=models.RESTRICT)
    title = models.CharField(max_length=128)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
