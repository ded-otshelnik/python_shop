from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.admin import ModelAdmin


class UserProfileAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)
        try:
            if form.is_valid():
                # Create a new user profile
                obj = form.save(commit=False)
                obj.set_password(form.cleaned_data["password"])
                obj.save()
                self.message_user(
                    request, "User created successfully", messages.SUCCESS
                )
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
