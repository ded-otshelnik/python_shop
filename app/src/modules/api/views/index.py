from django.http import HttpRequest
from django.shortcuts import render

from ..models import Product


def index(request: HttpRequest):
    """
    Index view for the shop application.
    This view can be used to render the homepage or a landing page.
    """
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "api/index.html", context=context)
