from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
)
from .models import Product, Category


def index(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()

    return HttpResponse("\n".join([str(product) for product in products]), status=200)


def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    try:
        product = Product.objects.get(id=product_id)
        return HttpResponse(str(product), status=200)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")


def category_detail(request: HttpRequest, category_id: int) -> HttpResponse:
    try:
        category = Category.objects.get(id=category_id)
        products = category.products.all()
        return HttpResponse("\n".join([str(product) for product in products]), status=200)
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category not found")
