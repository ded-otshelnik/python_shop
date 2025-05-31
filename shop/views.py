from django.http import HttpResponse


def index(request):
    """
    Index view for the shop application.
    This view can be used to render the homepage or a landing page.
    """
    return HttpResponse("Welcome to the Shop!")
