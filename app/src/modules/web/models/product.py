from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField("Category")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return ", ".join([self.name, str(self.price), str(self.stock)])

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price}, stock={self.stock})"

    class Meta:
        ordering = ("name",)
        verbose_name = "product"
        verbose_name_plural = "products"
