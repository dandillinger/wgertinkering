#!/usr/bin/env python

# Railway-specific settings for wger deployment
# This file extends the global settings with Railway-specific configurations

# Third Party
import environ
import os

# wger
from wger.settings_global import *

env = environ.Env(
    # set casting, default value
    DJANGO_DEBUG=(bool, False)
)

# Railway-specific configuration
DEBUG = env("DJANGO_DEBUG", default=False)

# Railway provides PostgreSQL by default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("PGDATABASE"),
        'USER': env.str("PGUSER"),
        'PASSWORD': env.str("PGPASSWORD"),
        'HOST': env.str("PGHOST"),
        'PORT': env.str("PGPORT", default="5432"),
    }
}

# Railway provides Redis for caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str("REDIS_URL", default="redis://localhost:6379/1"),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Railway static file configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files - Railway provides persistent storage
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security settings for Railway
SECRET_KEY = env.str("SECRET_KEY", default="your-secret-key-here")
ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
    env.str("RAILWAY_PUBLIC_DOMAIN", default=""),
]

# Railway URL configuration
SITE_URL = env.str("RAILWAY_PUBLIC_DOMAIN", default="https://your-app.railway.app")
WGER_SETTINGS['WGER_INSTANCE'] = SITE_URL

# Email configuration (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str("SMTP_HOST", default="")
EMAIL_PORT = env.int("SMTP_PORT", default=587)
EMAIL_USE_TLS = env.bool("SMTP_USE_TLS", default=True)
EMAIL_HOST_USER = env.str("SMTP_USER", default="")
EMAIL_HOST_PASSWORD = env.str("SMTP_PASSWORD", default="")

# Railway-specific middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise for static files
] + MIDDLEWARE

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging configuration for Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': 'level={levelname} ts={asctime} module={module} message={message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Disable Celery for Railway (optional - can be enabled if needed)
WGER_SETTINGS["USE_CELERY"] = False
WGER_SETTINGS["SYNC_EXERCISES_CELERY"] = False
WGER_SETTINGS["SYNC_EXERCISE_IMAGES_CELERY"] = False
WGER_SETTINGS["SYNC_EXERCISE_VIDEOS_CELERY"] = False
WGER_SETTINGS["SYNC_INGREDIENTS_CELERY"] = False

# Railway environment variables
WGER_SETTINGS["ALLOW_GUEST_USERS"] = env.bool("ALLOW_GUEST_USERS", default=True)
WGER_SETTINGS["ALLOW_REGISTRATION"] = env.bool("ALLOW_REGISTRATION", default=True)
WGER_SETTINGS["ALLOW_UPLOAD_VIDEOS"] = env.bool("ALLOW_UPLOAD_VIDEOS", default=False)

# CSRF settings for Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://your-app.railway.app',
]

# Security headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Silence system checks for Railway deployment
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
