from django.core.validators import MinValueValidator
from django.db import models

from django_project.extra.models import AuditModel


class Tag(AuditModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "tags"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Category(AuditModel):
    name = models.CharField(max_length=128, unique=True, verbose_name="Название")
    description = models.TextField(blank=True)

    class Meta:
        db_table = "categories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Product(AuditModel):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория"
    )
    name = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена"
    )
    stock = models.PositiveIntegerField(verbose_name="Кол-во на складе")
    is_active = models.BooleanField(default=True)

    tags = models.ManyToManyField(Tag, related_name="products")

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProductImage(AuditModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="%Y/%m/%d")

    class Meta:
        db_table = "product_images"

    def __str__(self):
        return self.image.name
