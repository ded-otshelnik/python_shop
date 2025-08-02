from django.urls import path
from .views import login, signup

urlpatterns = [
    path("users/login/", login.sign_in, name="login"),
    path("users/logout/", login.logout_view, name="logout"),
    path("users/profile/", login.get_user, name="profile"),
    path("users/register/", signup.create_user, name="signup"),
]
