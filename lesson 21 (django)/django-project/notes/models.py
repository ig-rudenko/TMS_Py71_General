from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Note(models.Model):

    user = models.ForeignKey(USER_MODEL, on_delete=models.RESTRICT)
    title = models.CharField(max_length=128, verbose_name="Заголовок", help_text="Не более 128 символов")
    content = models.TextField(verbose_name="Содержимое")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(
        upload_to="notes/%Y/%m", blank=True, null=True, verbose_name="Картинка", max_length=256
    )
    tags = models.ManyToManyField("Tag", blank=True)

    class Meta:
        ordering = ["-created_at"]
