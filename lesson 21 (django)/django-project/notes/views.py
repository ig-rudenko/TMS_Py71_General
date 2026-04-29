from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Substr
from django.db.models.query import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from notes.forms import CreateNoteForm
from notes.models import Note


def home_view(request):
    return render(request, "index.html")


def about_view(request):
    return render(request, "about.html")


# --------------------------------------- NOTES LIST ---------------------------------------


def notes_list_view(request):
    search = request.GET.get("search", "")
    page_number = request.GET.get("page", "1")
    per_page = 10

    notes_qs = Note.objects.all()
    if search:
        notes_qs = notes_qs.filter(Q(title__icontains=search) | Q(content__icontains=search))
    notes_qs = notes_qs.select_related("user")  # JOIN с users только для FK.
    notes_qs = notes_qs.prefetch_related("tags")  # JOIN только для M2M.
    notes_qs = notes_qs.annotate(short_content=Substr("content", 1, 200))
    notes_qs = notes_qs.order_by("-created_at")
    notes_qs = notes_qs.only("id", "title", "updated_at", "user__username")

    paginator = Paginator(notes_qs, per_page)
    page = paginator.get_page(page_number)

    return render(request, "posts/list.html", context={"page": page})


class NotesListView(ListView):
    paginate_by = 10
    template_name = "posts/list.html"

    def get_queryset(self):
        search = self.request.GET.get("search", "")

        notes_qs = Note.objects.all()
        if search:
            notes_qs = notes_qs.filter(Q(title__icontains=search) | Q(content__icontains=search))
        notes_qs = notes_qs.select_related("user")  # JOIN с users только для FK.
        notes_qs = notes_qs.prefetch_related("tags")  # JOIN только для M2M.
        notes_qs = notes_qs.annotate(short_content=Substr("content", 1, 200))
        notes_qs = notes_qs.order_by("-created_at")
        notes_qs = notes_qs.only("id", "title", "updated_at", "user__username")
        return notes_qs


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
            return redirect(resolve_url("notes-detail", note_id=note.id))

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
        return resolve_url("notes-detail", note_id=self.object.id)


# --------------------------------------- DETAIL NOTE ---------------------------------------


@login_required
def note_detail_view(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    # if request.user != note.user:
    #     raise Http404("Note does not exist")

    return render(request, "posts/detail.html", context={"note": note})
