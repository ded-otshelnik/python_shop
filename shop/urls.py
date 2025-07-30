from django.urls import path
from . import views
from .user import views as user_views
from .product import views as product_views

urlpatterns = [
    path("users/get_user/", user_views.get_user_by_username, name="get_user_by_username"),
    path("users/create_user/", user_views.create_user, name="create_user"),
    path("products/", product_views.index, name="product_index"),
    path(
        "products/<int:product_id>/", product_views.product_detail, name="product_detail"
    ),
    path(
        "categories/<int:category_id>/",
        product_views.category_detail,
        name="category_detail",
    ),
]
