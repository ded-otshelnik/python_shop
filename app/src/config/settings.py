# Django settings for python_shop project.

# Generated using djpro 0.0.1.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/5.0/ref/settings/

import environ
import os
import warnings

ENV_PATH_CONF = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(ENV_PATH_CONF, ".env.conf")):
    warnings.warn("Environment configuration file .env.conf not found. Check environment variable DJANGO_ENV.")
else:    
    environ.Env.read_env(os.path.join(ENV_PATH_CONF, ".env.conf"))

ENVIRONMENT = os.getenv("DJANGO_ENV", "dev")
print(f"Loading settings for environment: {ENVIRONMENT}")

if ENVIRONMENT == "prod":
    from .settings_prod import *
else:
    from .settings_dev import *
