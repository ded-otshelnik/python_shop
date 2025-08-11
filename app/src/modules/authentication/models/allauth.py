from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from utils import Logger

log = Logger.get_instance()


class AccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        User = get_user_model()
        return User()

    def _extract_email(self, data):
        # Google case
        if "email" in data:
            return data["email"]

        # Yandex case
        elif "default_email" in data:
            return data["default_email"]
        elif "emails" in data and isinstance(data["emails"], list):
            return data["emails"][0]

        raise ValueError("Email not found in social login data")

    def populate_email_address(self, request, sociallogin):
        """
        Override to ensure email address is created for the user.
        """
        email = self._extract_email(sociallogin.account.extra_data)

        verified = sociallogin.account.extra_data.get("verified_email", True)
        primary = sociallogin.account.extra_data.get("primary", True)
        EmailAddress.objects.get_or_create(
            user=sociallogin.user, email=email, verified=verified, primary=primary
        )

    def _extract_name(self, data):
        """
        Extracts the name from the social login data.
        """
        if "name" in data:
            return data["name"]
        elif "real_name" in data:
            return data["real_name"]

        # Yandex case
        elif "first_name" in data and "last_name" in data:
            return f"{data['first_name']} {data['last_name']}"

        # Google case
        elif "given_name" in data and "family_name" in data:
            return f"{data['given_name']} {data['family_name']}"
        return ""

    def populate_user(self, request, sociallogin, data):
        """
        Override to populate the user with additional data.
        """
        user = sociallogin.user
        user.email = self._extract_email(data)
        user.realname = self._extract_name(data)

        return user

    def save_user(self, request, sociallogin, form=None):
        # Create user and populate it with data from the social login
        user = super().save_user(request, sociallogin, form)
        user = self.populate_user(request, sociallogin, sociallogin.account.extra_data)
        user.save()

        # Ensure email address is created and associated with the user
        self.populate_email_address(request, sociallogin)
        return user
