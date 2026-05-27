from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from djoser.views import TokenCreateView
from rest_framework.generics import ListCreateAPIView

from django_project.extra.permissions import IsAdminOrCreateOnly
from .models import User
from .serializers import UserSerializer
from .swagger.schemas import api_token_create_docs


class ListCreateUserAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrCreateOnly]

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data["password"]))


@method_decorator(api_token_create_docs, name="post")
class CustomTokenCreateView(TokenCreateView):
    pass
