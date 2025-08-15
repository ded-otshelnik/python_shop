from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from allauth.account.models import EmailAddress


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        if UserProfile.objects.filter(email=email).exists():
            raise ValueError("A user with that email already exists")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is None:
            extra_fields["is_staff"] = False
        if extra_fields.get("is_superuser") is None:
            extra_fields["is_superuser"] = False
        if extra_fields.get("is_staff") and not extra_fields.get("is_superuser"):
            raise ValueError("Staff users must also be superusers.")

        user = self.model(email=email, **extra_fields)
        # set_password is used to hash the password
        # without it, the password will be stored as plain text
        # and validation will fail
        user.set_password(password)
        user.save()

        # ensure email address is created and associated with the user
        EmailAddress.objects.get_or_create(
            user=user, email=email, verified=True, primary=True
        )

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=155,
        unique=True,
    )
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    realname = models.CharField(max_length=50, blank=True, default="No real name")
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True, blank=True, null=True)

    objects = UserProfileManager()

    def __repr__(self):
        return f"UserProfile(email={self.email}, realname={self.realname})"

    def __str__(self):
        return f"{self.email} - {self.realname or 'No real name'}"

    @property
    def is_utc(self):
        return self.timezone == "UTC"
