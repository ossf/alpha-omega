import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from core import get_env_variable, to_bool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environment variables from a file
try:
    import dotenv

    dotenv.read_dotenv(os.path.join(BASE_DIR, ".env"))
except Exception:
    raise ImproperlyConfigured("A .env file was not found. Environment variables are not set.")

SECRET_KEY = get_env_variable("SECRET_KEY")
DEBUG = to_bool(get_env_variable("DEBUG"))

INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "taggit",
    "triage",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": get_env_variable("DATABASE_ENGINE"),
        "NAME": get_env_variable("DATABASE_NAME"),
        "USER": get_env_variable("DATABASE_USER"),
        "PASSWORD": get_env_variable("DATABASE_PASSWORD"),
        "HOST": get_env_variable("DATABASE_HOST"),
        "PORT": get_env_variable("DATABASE_PORT"),
        "OPTIONS": {"options": "-c statement_timeout=5000"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Los_Angeles"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Set up caching
DEFAULT_CACHE_TIMEOUT = 60 * 30  # 30 minutes
CACHES = {}
if to_bool(get_env_variable("ENABLE_CACHE")):
    if to_bool(get_env_variable("CACHE_USE_REDIS")):
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": get_env_variable("CACHE_REDIS_CONNECTION"),
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    "TIMEOUT": DEFAULT_CACHE_TIMEOUT,
                    "PASSWORD": get_env_variable("CACHE_REDIS_PASSWORD"),
                },
            }
        }
    else:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake",
                "TIMEOUT": DEFAULT_CACHE_TIMEOUT,
            },
        }

# Configure application logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": u"[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": u"%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose", "level": "WARNING"},
        #'appinsights': {
        #    'class': 'applicationinsights.django.LoggingHandler',
        #    'level': 'INFO',
        # },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "..", "logs", "omega-triage.log"),
            "maxBytes": 1024 * 1024 * 50,  # 50 MB
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "database-log": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "..", "logs", "database.log"),
            "maxBytes": 1024 * 1024 * 50,  # 50 MB
            "backupCount": 1,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": True,
        },
        "django": {
            "level": "WARNING",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "django.db": {
            "level": "DEBUG",
            "handlers": ["database-log"],
            "propagate": True,
        },
        "triage": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET = get_env_variable("TOOLSHED_BLOB_STORAGE_CONTAINER")
TOOLSHED_BLOB_STORAGE_URL_SECRET = get_env_variable("TOOLSHED_BLOB_STORAGE_URL")

OSSGADGET_PATH = get_env_variable("OSSGADGET_PATH")

AUTH_USER_MODEL = "auth.User"
