# Development settings
import os
import logging
import environ

from .settings_base import *

env = environ.Env(
    # default value
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(str, "*"),
    SQL_ENGINE=(str, "django.db.backends.sqlite3"),
    SQL_DATABASE=(str, "db.sqlite3"),
    SQL_USER=(str, "user"),
    SQL_PASSWORD=(str, "password"),
    SQL_HOST=(str, "localhost"),
    SQL_PORT=(str, "5432"),
)

environ.Env.read_env(os.path.join(ENV_PATH, ".env.dev"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

# Allowed hosts
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")

# Email settings for development (console backend)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE"),
        "NAME": env("SQL_DATABASE"),
        "USER": env("SQL_USER"),
        "PASSWORD": env("SQL_PASSWORD"),
        "HOST": env("SQL_HOST"),
        "PORT": env("SQL_PORT"),
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]
SECURE_SCHEME_HEADERS = {
    "X-FORWARDED-PROTO": "https",
}

# Custom user model
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*", "realname"]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_UNIQUE_EMAIL = True

SOCIALACCOUNT_PROVIDERS = {
    "Google API": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID"),
            "secret": env("GOOGLE_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
            "birthday",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    },
    "Yandex API": {
        "APP": {
            "client_id": env("YANDEX_CLIENT_ID"),
            "secret": env("YANDEX_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "login:info",
            "login:avatar",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}

# Custom settings
PAYMENT_GATEWAY_URL = env("PAYMENT_GATEWAY_URL")
# CERT_PUBLIC_KEY_PATH = env("CERT_PUBLIC_KEY_PATH")
# CERT_PRIVATE_KEY_PATH = env("CERT_PRIVATE_KEY_PATH")
