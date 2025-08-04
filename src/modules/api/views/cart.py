from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from utils.logging import Logger

from ..models import Cart, Product


log = Logger.get_instance()


@login_required
def get_cart(request: HttpRequest) -> HttpResponse:
    cart = Cart.objects.filter(user=request.user).first()
    context = {"cart": cart}
    return render(request, "api/order/cart.html", context)


@login_required
def add_to_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)

    product = Product.objects.get(id=product_id)
    if not product:
        raise Http404("Product not found")

    cart.add_or_increment(product)

    return redirect(f"/api/shop/products/{product_id}/", request=request)
