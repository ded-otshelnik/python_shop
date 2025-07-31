from django.contrib import admin
from .product.models import Product
from .order.models import Order, OrderItem
from .models import UserProfile
from .user.admin import UserProfileAdmin


# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = "Python Shop Admin"
