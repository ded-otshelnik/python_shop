import json
from django.http import (
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponse,
    HttpRequest,
)
from django.views.decorators.http import require_POST, require_GET
from ..models import UserProfile


@require_GET
def get_user_by_username(request: HttpRequest):
    """
    Retrieve a user by their username.

    :param username: The username of the user to retrieve.
    :return: User object if found, None otherwise.
    """
    try:
        username = request.GET.get("username")
        username = username.strip() if username else None
        if not username:
            return HttpResponseBadRequest("Username parameter is required")

        user = UserProfile.objects.find_by_username(username=username)
        return HttpResponse(user)
    except UserProfile.DoesNotExist:
        return HttpResponseNotFound("User not found")


@require_POST
def create_user(request: HttpRequest):
    """
    Create a new user.
    """
    try:
        post_data_json = json.loads(request.body.decode("utf-8"))
        UserProfile.objects.create_user(**post_data_json)
        return HttpResponse("User created successfully")
    except Exception as e:
        return HttpResponseBadRequest(f"Error creating user: {str(e)}")
