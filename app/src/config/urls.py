# URL configuration for python_shop project.

# For more information please see:
# https://docs.djangoproject.com/en/5.0/topics/http/urls/

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Django Admin Site
    # Including a new module
    path("", include("modules.web.urls")),
    path("auth/", include("modules.authentication.urls")),
    path("auth/", include("allauth.urls")),
    path("auth/social/", include("allauth.socialaccount.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
