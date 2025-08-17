import requests
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from ..models.order import Order

from utils import Logger

log = Logger.get_instance("orders")


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
        order = Order.objects.get(id=order_id, customer=request.user)
        payment_id = order.payment_id

        response = requests.get(
            f"{settings.PAYMENT_GATEWAY_URL}?payment_id={payment_id}",
            verify=False,
            timeout=30,
        )

        if response.status_code != 200:
            return HttpResponseNotFound("Payment information not found")

        payment = response.json()
        context = {"order": order, "payment": payment["payment_info"]}
        return render(request, "web/order/order.html", context)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order not found")
