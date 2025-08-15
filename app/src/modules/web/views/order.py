from ..models.order import Order
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    orders = (
        Order.objects.filter(customer=request.user)
        .prefetch_related("orderitem_set")
        .order_by("-created_at")
    )
    context = {"orders": orders}
    return render(request, "web/order/order_history.html", context)


@login_required
def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    try:
        order = Order.objects.prefetch_related("orderitem_set").get(
            id=order_id, customer=request.user
        )
        context = {"order": order}
        return render(request, "web/order/order.html", context)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order not found")
