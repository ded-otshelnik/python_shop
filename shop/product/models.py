from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField("Category", blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return ", ".join([self.name, str(self.price), str(self.stock)])


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
