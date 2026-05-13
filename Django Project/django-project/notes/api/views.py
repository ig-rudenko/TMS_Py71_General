from django.db.models.functions import Substr
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from notes.models import Note
from .filters import NoteFilter
from .permissions import IsNoteOwnerOrReadOnly
from .serializers import NoteSerializer, NoteListSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def notes_api_view(request):
    if request.method == "GET":
        notes = Note.objects.all()[:10]
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    else:
        print("request.data:", request.data)
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=request.user)  # create new note
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def note_detail_api_view(request, note_id: int):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "DELETE":
        note.delete()
        return Response(NoteSerializer(note).data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = NoteSerializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # update
        return Response(NoteSerializer(note).data)

    elif request.method == "PATCH":
        serializer = NoteSerializer(note, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(NoteSerializer(note).data)

    # method == "GET"
    return Response(NoteSerializer(note).data)


class NoteListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = NoteFilter
    queryset = (
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NoteListSerializer
        return NoteSerializer


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsNoteOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "note_id"
    queryset = (
        Note.objects.all()
        .select_related("user")
        .only(
            "title",
            "user",
            "image",
            "content",
            "created_at",
            "updated_at",
            "user__username",
            "user__email",
        )
    )
    serializer_class = NoteSerializer
