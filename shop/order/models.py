from django.db import models
from ..product.models import Product
from ..user.models import UserProfile


class Order(models.Model):
    customer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="orders"
    )
    customer_email = models.EmailField()
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default="Pending")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.customer.username} - {self.customer_email}, {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.product.name} ({self.quantity})"
