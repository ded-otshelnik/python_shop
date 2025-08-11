from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from ..models import UserProfile

from utils import Logger

log = Logger.get_instance()


class SignupForm(AllauthSignupForm):
    def save(self, request, commit=False):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save(request)

        # Add your own processing here.
        log.info(f"Creating user with email: {user.email}")
        user.email = self.cleaned_data["email"]
        user.realname = self.cleaned_data.get("realname", "No real name")
        if user.realname == "No real name":
            realname = (
                self.cleaned_data["given_name"] + " " + self.cleaned_data["family_name"]
            )
            user.realname = realname if realname.strip() else user.realname

        log.info(f"User {user.email} created with real name {user.realname}")
        user.save()

        # You must return the original result.
        return user

    def signup(self, request, user, commit=False):
        log.info(f"Signing up user: {user.email}")
        user.email = self.cleaned_data["email"]
        user.realname = self.cleaned_data.get("realname", "No real name")
        if user.realname == "No real name":
            realname = (
                self.cleaned_data["given_name"] + " " + self.cleaned_data["family_name"]
            )
            user.realname = realname if realname.strip() else user.realname

        user.birthday = self.cleaned_data.get("birthday", None)
        user.phone = self.cleaned_data.get("phone", None)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()
        return user
