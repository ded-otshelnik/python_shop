from django.contrib.auth import authenticate, login
from django.http import (
    HttpResponseRedirect,
    HttpRequest,
)
from django.shortcuts import render
from django.views.decorators.http import (
    require_http_methods,
)

from ..forms import SignupForm


@require_http_methods(["GET", "POST"])
def create_user(request: HttpRequest):
    """
    Create a new user.
    """
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Check if the user is created successfully
            user = authenticate(
                username=user.username, password=form.cleaned_data["password"]
            )
            if user is None:
                form.add_error(None, "User creation failed. Please try again.")
            else:
                login(request, user)
                return HttpResponseRedirect("/api/shop")
        else:
            form.add_error(None, "Invalid user data")
    else:
        form = SignupForm(None)
    return render(request, "authentication/signup.html", {"form": form})
