from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='shop_index'),  # Home page
    path('products/', catalog, name='catalog'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
]