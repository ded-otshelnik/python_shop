from django import forms
from allauth.account.forms import LoginForm as AllauthLoginForm
from django.contrib.auth import get_user_model

from utils import Logger

log = Logger.get_instance()


class LoginForm(AllauthLoginForm):
    model = get_user_model()

    def login(self, request, **kwargs):
        user = request.user
        if not user:
            log.error("No user provided for login.")
            raise forms.ValidationError("No user provided for login.")
        # Custom login logic can be added here if needed
        log.info(f"Logging in user: {user.email}")
        cleaned_data = self.clean()
        log.debug(f"Cleaned data: {cleaned_data}")
        return super().login(request, user)

    def clean(self):
        # Custom validation logic can be added here if needed
        cleaned_data = super(LoginForm, self).clean()
        if not cleaned_data:
            # If no data is provided, raise a validation error
            log.error("No data provided in login form.")
            self.add_error(None, "No data provided.")
            raise forms.ValidationError("No data provided.")
        log.debug("Validating login form")
        log.debug(f"Cleaned data: {cleaned_data}")

        email = cleaned_data.get("login", None)
        password = cleaned_data.get("password", None)

        if not email or not password:
            self.add_error("Both email and password are required.")
            raise forms.ValidationError("Both email and password are required.")

        if not self.model.objects.filter(email=email).exists():
            self.add_error("User with this email does not exist.")
            raise forms.ValidationError("User with this email does not exist.")

        return cleaned_data
