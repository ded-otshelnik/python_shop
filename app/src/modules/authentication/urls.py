from django.urls import path
from .views import login, signup

urlpatterns = [
    # path("login/", login.sign_in, name="login"),
    # path("logout/", login.logout_view, name="logout"),
    path("profile/", login.get_user, name="profile"),
    # path("signup/", signup.create_user, name="signup"),
]
