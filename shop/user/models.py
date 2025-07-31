from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)

        # set_password is used to hash the password
        # without it, the password will be stored in plain text
        # and validation will fail
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(username, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    password = models.CharField(
        max_length=128,
        help_text="Required. 128 characters or fewer.",
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    realname = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True, blank=True, null=True)

    objects = UserProfileManager()

    def __repr__(self):
        return f"{self.username} - {self.realname or 'No real name'}"

    def __str__(self):
        return f"{self.username} - {self.realname or 'No real name'}"
