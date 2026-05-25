from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView

from catalog.filters import CategoryFilter, ProductFilter
from catalog.services import create_product, update_product
from django_project.extra.permissions import IsAdminOrReadOnly
from catalog.models import Category, Product
from catalog.serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductSerializer,
    ImageUploadSerializer,
)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = CategoryFilter


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        create_product(serializer.validated_data)

    def perform_update(self, serializer):
        update_product(serializer.instance, serializer.validated_data)


class ImageUploadView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ImageUploadSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = ImageUploadSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
