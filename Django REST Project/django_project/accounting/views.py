from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListCreateAPIView

from django_project.extra.permissions import IsAdminOrCreateOnly
from .models import User
from .serializers import UserSerializer


class ListCreateUserAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrCreateOnly]

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data["password"]))
