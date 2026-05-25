from rest_framework.routers import DefaultRouter

from catalog.views import CategoryViewSet, ProductsViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductsViewSet, basename="product")
