from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
    HttpRequest,
)
from django.shortcuts import render
from django.views.decorators.http import (
    require_GET,
    require_http_methods,
)

from .forms import RegistrationForm, LoginForm


@login_required
@require_GET
def get_user(request: HttpRequest):
    """
    Retrieve a user by their username.

    :param username: The username of the user to retrieve.
    :return: User object if found, None otherwise.
    """
    context = {"user": request.user}
    return render(request, "user/user.html", context)


@require_http_methods(["GET", "POST"])
def sign_in(request: HttpRequest):
    """
    Handle user login.
    """
    if request.method == "POST":
        details = LoginForm(request.POST)

        if details.is_valid():
            user_details = details.cleaned_data
            user = authenticate(request, **user_details)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/shop")

        details.add_error(None, "Invalid credentials")
        return render(request, "registration/login.html", {"form": details})
    else:
        form = LoginForm(None)
        return render(request, "registration/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def create_user(request: HttpRequest):
    """
    Create a new user.
    """
    if request.method == "POST":
        details = RegistrationForm(request.POST)

        if details.is_valid():
            user = details.save(commit=False)
            user.set_password(details.cleaned_data["password"])
            user.save()
            login(request, user)
            return HttpResponseRedirect("/shop")
        else:
            details.add_error(None, "Invalid user data")
            return render(request, "registration/signup.html", {"form": details})
    else:
        form = RegistrationForm(None)
        return render(request, "registration/signup.html", {"form": form})


@require_GET
def logout_view(request: HttpRequest):
    """
    Log out the user.
    """
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/shop")
