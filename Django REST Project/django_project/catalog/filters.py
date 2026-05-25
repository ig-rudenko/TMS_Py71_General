from django_filters.rest_framework import filterset as drf_filterset, filters

from .models import Category, Product


class CategoryFilter(drf_filterset.FilterSet):
    name = filters.CharFilter(lookup_expr="iexact")
    description = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["name", "description"]


class ProductFilter(drf_filterset.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    stock = filters.RangeFilter(lookup_expr="gte")
    category = filters.CharFilter("category__name", lookup_expr="iexact")
    price = filters.RangeFilter(lookup_expr="gte")

    class Meta:
        model = Product
        fields = ["name", "description", "is_active", "stock", "category", "price"]
