from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Note(models.Model):

    user = models.ForeignKey(USER_MODEL, on_delete=models.RESTRICT)
    title = models.CharField(
        max_length=128,
        verbose_name="Заголовок",
        help_text="Не более 128 символов",
        validators=[MinLengthValidator(3)],
    )
    content = models.TextField(verbose_name="Содержимое")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(
        upload_to="notes/%Y/%m", blank=True, null=True, verbose_name="Картинка", max_length=256
    )
    tags = models.ManyToManyField("Tag", blank=True)

    class Meta:
        ordering = ["-created_at"]
        # indexes = [
        #     GinIndex(
        #         SearchVector("title", "content", config="russian"),
        #         name="search_fts_idx",
        #     ),
        #     GinIndex(
        #         name="search_trgm_idx",
        #         fields=["title", "content"],
        #         opclasses=["gin_trgm_ops", "gin_trgm_ops"],
        #     ),
        # ]


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1024, validators=[MinLengthValidator(3)], verbose_name="Комментарий")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User: {self.user_id} | Note: {self.note_id} | Text: {self.text}"

    class Meta:
        ordering = ["-created_at"]
