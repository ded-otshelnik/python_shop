from django.urls import path

from . import views
from .user import views as user_views
from .product import views as product_views


urlpatterns = [
    path("", views.index, name="shop_index"),
    path("accounts/login/", user_views.sign_in, name="login"),
    path("accounts/logout/", user_views.logout_view, name="logout"),
    path("accounts/signup/", user_views.create_user, name="signup"),
    path("accounts/profile/", user_views.get_user, name="profile"),
    path(
        "catalog/product/<int:product_id>/",
        product_views.product_detail,
        name="product_detail",
    ),
]
