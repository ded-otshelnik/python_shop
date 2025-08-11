from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from ..models import Product


@require_http_methods(["GET", "POST"])
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
            return HttpResponseRedirect("/auth/login/?next=/cart/{}/".format(product_id))
        # For now, we just redirect to the product detail page
        return HttpResponseRedirect(f"/cart/{product_id}/")
