# Production settings
import os
from pathlib import Path
import environ

env = environ.Env(
    # default value
    DEBUG=(bool, False),
)

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

environ.Env.read_env(os.path.join(ENV_PATH, ".env.prod"))

SECRET_KEY = env("SECRET_KEY")

# Debug mode
DEBUG = env("DEBUG")

from .settings_base import *

# Allowed hosts
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Email backend (SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

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

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SCHEME_HEADERS = {
    "X-FORWARDED-PROTO": "https",
}

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
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
