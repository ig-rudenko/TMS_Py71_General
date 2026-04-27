from django import forms

from .models import Note


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "image", "tags"]
