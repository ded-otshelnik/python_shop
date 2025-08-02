from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET

from ..forms import LoginForm

@login_required
@require_GET
def get_user(request: HttpRequest):
    """
    Retrieve a user by their username.

    :param username: The username of the user to retrieve.
    :return: User object if found, None otherwise.
    """
    context = {"user": request.user}
    return render(request, "authentication/user.html", context)


@require_http_methods(["GET", "POST"])
def sign_in(request: HttpRequest):
    """
    Handle user login.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user_details = form.cleaned_data
            user = authenticate(request, **user_details)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/api/shop")

        form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm(None)
    return render(request, "authentication/login.html", {"form": form})

@require_GET
def logout_view(request: HttpRequest):
    """
    Log out the user.
    """
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/api/shop")
