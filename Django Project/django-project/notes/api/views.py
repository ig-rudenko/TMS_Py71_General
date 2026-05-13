from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note
from .serializers import NoteDetailSerializer, NoteCreateUpdateSerializer, NoteSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def notes_api_view(request):
    if request.method == "GET":
        notes = Note.objects.all()[:10]
        serializer = NoteDetailSerializer(notes, many=True)
        return Response(serializer.data)

    else:
        print("request.data:", request.data)
        serializer = NoteCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=request.user)  # create new note
        return Response(NoteDetailSerializer(note).data, status=status.HTTP_201_CREATED)


class NoteListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        notes = Note.objects.all()[:10]
        serializer = NoteDetailSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("request.data:", request.data)
        serializer = NoteCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=request.user)  # create new note
        return Response(NoteDetailSerializer(note).data, status=status.HTTP_201_CREATED)


class NoteListCreateGenericAPIView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NoteSerializer

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("request.data:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=request.user)  # create new note
        return Response(self.get_serializer(note), status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def note_detail_api_view(request, note_id: int):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "DELETE":
        note.delete()
        return Response(NoteDetailSerializer(note).data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = NoteCreateUpdateSerializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # update
        return Response(NoteDetailSerializer(note).data)

    elif request.method == "PATCH":
        serializer = NoteCreateUpdateSerializer(note, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(NoteDetailSerializer(note).data)

    # method == "GET"
    return Response(NoteDetailSerializer(note).data)
