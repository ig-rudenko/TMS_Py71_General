from dataclasses import dataclass

from celery import shared_task
from django.db.models.functions import Substr
from rest_framework.pagination import PageNumberPagination

from .api.serializers import NoteSerializer
from .models import Note
from .services import NotesCache


@dataclass
class FakeRequest:
    page: int

    def build_absolute_uri(self):
        return "http://example.com"


class TaskPageNumberPagination(PageNumberPagination):

    def get_page_number(self, request, paginator):
        return request.page

    def get_page_size(self, request):
        return self.page_size


@shared_task
def create_notes_cache():
    qs = (
        Note.objects.all()
        .select_related("user")
        .prefetch_related("tags")
        .only(
            "title",
            "user",
            "image",
            "created_at",
            "updated_at",
            "user__username",
            "user__email",
        )
        .annotate(content_preview=Substr("content", 1, 200))
    )

    for page_num in range(1, NotesCache.max_page_cache_size + 1):
        paginator = TaskPageNumberPagination()
        page = paginator.paginate_queryset(qs, FakeRequest(page_num), view=NotesCache)
        serializer = NoteSerializer(page, many=True)
        response = paginator.get_paginated_response(serializer.data)

        NotesCache({"page": str(page_num)}).set(response.data)
