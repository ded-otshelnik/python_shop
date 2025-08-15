from .cart import get_cart, add_to_cart
from .category import catalog
from .category import category_detail
from .index import index
from .product import product_detail
from .checkout import CheckoutView
from .order import order_history, order_detail

__all__ = [
    "get_cart",
    "add_to_cart",
    "catalog",
    "CheckoutView",
    "index",
    "category_detail",
    "product_detail",
    "order_history",
    "order_detail",
]
