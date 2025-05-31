from django.http import Http404, HttpResponseBadRequest
from ..models import User

USER_FORMAT = "{username} <{email}>"


def get_user_by_username(username):
    """
    Retrieve a user by their username.

    :param username: The username of the user to retrieve.
    :return: User object if found, None otherwise.
    """
    try:
        user = User.objects.get(username=username)
        return USER_FORMAT % (user.username, user.email)
    except User.DoesNotExist:
        return Http404("User not found")


def get_user_by_email(email):
    """
    Retrieve a user by their email.

    :param email: The email of the user to retrieve.
    :return: User object if found, None otherwise.
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return Http404("User not found")


def create_user(username, email, password):
    """
    Create a new user.

    :param username: The username for the new user.
    :param email: The email for the new user.
    :param password: The password for the new user.
    :return: User object if created successfully, None otherwise.
    """
    try:
        user = User.create_user(username=username, email=email, password=password)
        return user
    except Exception as e:
        return HttpResponseBadRequest(f"Error creating user: {str(e)}")
