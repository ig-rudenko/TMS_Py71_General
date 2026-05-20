from rest_framework.viewsets import ModelViewSet

from django_project.extra.permissions import IsAdminOrReadOnly
from catalog.models import Category
from catalog.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
