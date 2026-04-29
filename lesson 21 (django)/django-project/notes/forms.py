from django import forms
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Note


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "image", "tags"]
        widgets = {
            "content": WysiwygWidget,
        }
