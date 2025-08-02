from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET
from django.shortcuts import render

from ..models import Product

@require_GET
def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    try:
        product = Product.objects.prefetch_related("categories").get(id=product_id)
        categories = ", ".join(map(str, product.categories.all()))
        context = {"product": product, "categories": categories}
        return render(request, "api/product/product.html", context)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")
