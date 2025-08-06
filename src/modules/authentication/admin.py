from django.contrib import admin
from .models import UserProfile, UserProfileAdmin
from allauth.account.decorators import secure_admin_login

# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = "Python Shop Admin"
admin.site.site_title = "Python Shop Admin Portal"
admin.site.index_title = "Welcome to the Python Shop Admin Portal"