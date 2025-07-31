from .base import *

import environ
import os


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
FIXTURE_ROOT = os.path.join(BASE_DIR, "fixtures")
