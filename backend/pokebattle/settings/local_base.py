from .base import *  # noqa
from decouple import config  # noqa


DEBUG = True

HOST = "http://localhost:8000"

SECRET_KEY = "secret"  # nosec

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": base_dir_join("db.sqlite3"),
    }
}

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

AUTH_PASSWORD_VALIDATORS = []  # allow easy passwords only on local

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Email
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = config("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = config("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(levelname)-8s [%(asctime)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "celery": {"handlers": ["console"], "level": "INFO"},
    },
}

JS_REVERSE_JS_MINIFY = False
