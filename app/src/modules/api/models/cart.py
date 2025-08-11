from django.db import models
from ...authentication.models import UserProfile


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField("Product", through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart of user {self.user.email} created at {self.created_at}"

    def __repr__(self):
        return f"Cart(user={self.user.email}, created_at={self.created_at})"

    def add_or_increment(self, product):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self, product=product, defaults={"quantity": 1}
        )

        # If the item already exists, increment the quantity
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    def remove_or_decrement(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            raise ValueError("Product not in cart")

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart} - {self.product.name} ({self.quantity})"

    def __repr__(self):
        return f"CartItem({self.cart}, {self.product}, {self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity
