from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from notes.filters import filter_notes_list
from notes.forms import CreateNoteForm, CommentForm
from notes.models import Note, Comment


def home_view(request):
    return render(request, "index.html")


def about_view(request):
    return render(request, "about.html")


# --------------------------------------- NOTES LIST ---------------------------------------


def notes_list_view(request):
    search = request.GET.get("search", "")
    page_number = request.GET.get("page", "1")
    per_page = 10

    notes_qs = filter_notes_list(search)

    paginator = Paginator(notes_qs, per_page)
    page = paginator.get_page(page_number)

    return render(request, "posts/list.html", context={"page": page})


class NotesListView(ListView):
    paginate_by = 10
    template_name = "posts/list.html"

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        return filter_notes_list(search)


# --------------------------------------- CREATE NOTE ---------------------------------------


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
            note.tags.set(form.cleaned_data["tags"])
            return redirect(resolve_url("notes:detail", note_id=note.id))

    return render(request, "posts/create.html", context={"form": form})


@method_decorator(login_required, name="dispatch")
class NoteCreateView(CreateView):
    template_name = "posts/create.html"
    form_class = CreateNoteForm

    def form_valid(self, form):
        self.object = Note.objects.create(
            title=form.cleaned_data["title"],
            content=form.cleaned_data["content"],
            image=form.cleaned_data["image"],
            user=self.request.user,
        )
        self.object.tags.set(form.cleaned_data["tags"])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return resolve_url("notes:detail", note_id=self.object.id)


# --------------------------------------- DETAIL NOTE ---------------------------------------


@login_required
def note_detail_view(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    page_number = request.GET.get("page", "1")
    per_page = 1

    paginator = Paginator(Comment.objects.filter(note=note), per_page)
    page = paginator.get_page(page_number)

    return render(
        request,
        "posts/detail.html",
        context={
            "note": note,
            "comment_form": CommentForm(),
            "comments_page": page,
        },
    )


# --------------------------------------- COMMENTS ---------------------------------------


@login_required
def create_note_comment(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                note=note,
                text=form.cleaned_data["text"],
            )

            return redirect(resolve_url("notes:detail", note_id=note.id) + "#comments")

    return render(
        request,
        "posts/detail.html",
        context={"note": note, "comment_form": form},
    )
