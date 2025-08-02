from django.db import models
from ...authentication.models import UserProfile

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField("Product", through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username} created at {self.created_at}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cart} - {self.product.name} ({self.quantity})"

    def __repr__(self):
        return f"CartItem({self.cart}, {self.product}, {self.quantity})"