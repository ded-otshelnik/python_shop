from ..models.order import Order, OrderItem, Cart, CartItem
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    orders = (
        Order.objects.filter(customer=request.user.profile)
        .prefetch_related("orderitem_set")
        .order_by("-created_at")
    )
    context = {"orders": orders}
    return render(request, "api/order/order_history.html", context)


@login_required
def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    try:
        order = Order.objects.prefetch_related("orderitem_set").get(
            id=order_id, customer=request.user.profile
        )
        context = {"order": order}
        return render(request, "api/order/order.html", context)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order not found")
