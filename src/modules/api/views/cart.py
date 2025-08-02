from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Cart


@login_required
def cart_view(request: HttpRequest) -> HttpResponse:
    cart = Cart.objects.filter(user=request.user.profile).first()
    context = {"cart": cart}
    return render(request, "api/order/cart.html", context)
