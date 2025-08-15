from django.contrib.auth import login
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
            user = form.save()
            login(request, user)
            if request.GET.get("next"):
                return HttpResponseRedirect(request.GET.get("next"))
            return HttpResponseRedirect("/")
    else:
        form = SignupForm(None)
    return render(request, "account/signup.html", {"form": form})
