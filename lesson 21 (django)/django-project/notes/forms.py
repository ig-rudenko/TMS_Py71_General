from django import forms

from .models import Note, Comment


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "image", "tags"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }
