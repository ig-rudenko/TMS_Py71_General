from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from django_project.extra.models import AuditModel

User = get_user_model()


class Cart(AuditModel):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())


class CartItem(AuditModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'cart_items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
