from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="shop_index"),
    path("cart/", get_cart, name="cart"),
    path("cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("catalog/", catalog, name="catalog"),
    path("catalog/<int:product_id>/", product_detail, name="product_detail"),
    path("categories/<int:category_id>/", category_detail, name="category_detail"),
    path("orders/", order_history, name="order_history"),
    path("orders/<int:order_id>/", order_detail, name="order_detail"),
]
