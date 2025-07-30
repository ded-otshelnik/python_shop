from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest):
    """
    Index view for the shop application.
    This view can be used to render the homepage or a landing page.
    """
    response = f"""
    Request Method: {request.method}
    Request Path: {request.path}
    Request Headers: {request.headers}
    Request Body: {request.body.decode('utf-8') if request.body else 'No body'}
    Request GET Parameters: {request.GET.dict()}
    Request POST Parameters: {request.POST.dict()}
    """
    return HttpResponse(response)


def health_check(request: HttpRequest) -> HttpResponse:
    """
    Health check endpoint to verify that the application is running.
    This can be used by load balancers or monitoring tools.
    """
    return HttpResponse("OK", status=200)
