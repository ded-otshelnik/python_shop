from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import render

from ..models import Product
from utils.logging import Logger

log = Logger.get_instance()


@require_GET
def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method == "GET":
        try:
            product = Product.objects.prefetch_related("categories").get(id=product_id)
            categories = ", ".join(map(str, product.categories.all()))
            context = {"product": product, "categories": categories}
            return render(request, "api/product/product.html", context)
        except Product.DoesNotExist:
            return HttpResponseNotFound("Product not found")
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                "/api/shop/login/?next=/api/shop/cart/{}/".format(product_id)
            )
        log.debug(f"Product {product_id} added to cart by user {request.user}")
        # For now, we just redirect to the product detail page
        return HttpResponseRedirect(f"/api/shop/cart/{product_id}/")
