from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    """
    Index view for the shop application.
    This view can be used to render the homepage or a landing page.
    """
    return render(request, "web/index.html")
