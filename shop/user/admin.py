from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)
        try:
            user = UserProfile.objects.create_user(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
