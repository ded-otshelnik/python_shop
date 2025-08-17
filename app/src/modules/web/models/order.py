from django.db import models

from .cart import Cart
from ...authentication.models import UserProfile


class OrderStatus(models.TextChoices):
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class OrderManager(models.Manager):
    def create(self, cart: Cart, payment_id: int) -> "Order":
        order = Order(customer=cart.user, payment_id=payment_id)
        order.save()
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity
            )

        cart.clear_cart()
        order.save()
        return order


class Order(models.Model):
    customer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.IN_PROGRESS,
    )
    payment_id = models.IntegerField(editable=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.orderitem_set.all())

    def __repr__(self):
        return f"Order(customer={self.customer.email}, order_date={self.order_date})"

    def __str__(self):
        return f"Order(customer={self.customer.email}, order_date={self.order_date})"


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return ", ".join(
            [
                f"OrderItem(order={self.order.id}",
                f"product={self.product.name}",
                f"quantity={self.quantity})",
            ]
        )

    def __repr__(self):
        return ", ".join(
            [
                f"OrderItem(order={self.order.id}",
                f"product={self.product.name}",
                f"quantity={self.quantity})",
            ]
        )

    def total_price(self):
        return self.product.price * self.quantity
