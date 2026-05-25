from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from django_project.extra.models import AuditModel

User = get_user_model()


class Order(AuditModel):
    class Status(models.TextChoices):
        WAITING = "WAITING"
        PAID = "PAID"
        CANCELED = "CANCELED"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(choices=Status.choices, max_length=32, default=Status.WAITING)  # noqa
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ пользователя {self.user.username} - {self.status}"


class OrderItem(AuditModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="order_items")
    product_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])

    class Meta:
        db_table = "order_items"
        ordering = ["-created_at"]

    @property
    def total_price(self):
        return self.product_price * self.quantity
