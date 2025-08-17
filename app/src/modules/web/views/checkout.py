import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


from ..models import Order, Cart
from ..forms import CheckoutForm
from utils import Logger

log = Logger.get_instance("checkout")


class CheckoutView(TemplateView):
    template_name = "web/order/checkout.html"

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart.objects.get(user=request.user)
        context["form"] = CheckoutForm(request.POST or None)
        return context

    @method_decorator(login_required)
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(request)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(request)

        cart = context.get("cart")
        if not cart:
            return HttpResponseNotFound("Cart not found")

        form = CheckoutForm(request.POST)
        payment = None

        if form.is_valid():
            cleaned_data = form.cleaned_data

            payload = {
                "user_id": request.user.id,
                "amount": context["cart"].total_price,
                "payment_method": cleaned_data.get("payment_method"),
                "currency": "RUB",
            }

            try:
                response = requests.post(
                    settings.PAYMENT_GATEWAY_URL,
                    json=payload,
                    verify=False,  # Skip SSL certificate verification
                    timeout=30,
                    headers={"Content-Type": "application/json"},
                )
            except requests.exceptions.SSLError as e:
                messages.error(request, f"Payment service unavailable: {str(e)}")
                return self.render_to_response(context)

            if response.status_code == 201 and response.json().get("payment_id"):
                payment = response.json()
                log.debug(f"Payment created successfully: {payment}")
            else:
                messages.error(request, f"Payment failed: {response.content}")
                return self.render_to_response(context)
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
            return self.render_to_response(context)

        order = Order.objects.create(cart, payment.get("payment_id"))
        if not order:
            return HttpResponseNotFound("Order creation failed")

        message = f"Order #{order.id} created successfully!"
        messages.success(request, message)

        return HttpResponseRedirect("/")
