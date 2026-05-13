from rest_framework import serializers

from notes.models import Note


class NoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "user", "image", "created_at", "updated_at"]


class NoteCreateUpdateSerializer(serializers.ModelSerializer):
    image = serializers.CharField(max_length=256)

    class Meta:
        model = Note
        fields = ["title", "content", "image"]


class NoteSerializer(serializers.ModelSerializer):
    image = serializers.CharField(max_length=256)

    class Meta:
        model = Note
        fields = ["id", "title", "content", "user", "image", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
