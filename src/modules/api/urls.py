from django.urls import path

from .views import (
    index,
    get_cart,
    add_to_cart,
    catalog,
    product_detail,
    category_detail
)

urlpatterns = [
    path("", index, name="shop_index"),
    path("cart/", get_cart, name="cart"),
    path("cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("products/", catalog, name="catalog"),
    path("products/<int:product_id>/", product_detail, name="product_detail"),
    path("categories/<int:category_id>/", category_detail, name="category_detail"),
]
