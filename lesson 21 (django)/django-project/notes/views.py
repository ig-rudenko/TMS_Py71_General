from django.contrib.auth.decorators import login_required, login_not_required
from django.db.models.functions import Substr
from django.http import Http404
from django.shortcuts import render, redirect, resolve_url

from notes.forms import CreateNoteForm
from notes.models import Note


def home_view(request):
    return render(request, "index.html")


def about_view(request):
    return render(request, "about.html")


@login_required
def notes_list_view(request):
    notes_qs = Note.objects.filter(user=request.user).select_related("user")  # JOIN с users
    notes_qs = notes_qs.annotate(short_content=Substr("content", 1, 200))
    notes_qs = notes_qs.order_by("-created_at")
    notes_qs = notes_qs[:10]  # Первые 10 заметок
    notes_qs = notes_qs.only("id", "title", "updated_at", "user__username")

    return render(request, "posts/list.html", context={"notes_qs": notes_qs})


@login_required
def note_create_view(request):
    form = CreateNoteForm()

    if request.method == "POST":
        form = CreateNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = Note.objects.create(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                image=form.cleaned_data["image"],
                user=request.user,
            )
            return redirect(resolve_url("notes-detail", note_id=note.id))

    return render(request, "posts/create.html", context={"form": form})


@login_required
def note_detail_view(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    if request.user != note.user:
        raise Http404("Note does not exist")

    return render(request, "posts/detail.html", context={"note": note})
