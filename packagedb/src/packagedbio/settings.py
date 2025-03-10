#
# Copyright (c) nexB Inc. and others. All rights reserved.
# purldb is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/purldb for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import sys
from pathlib import Path

import environ

PROJECT_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = PROJECT_DIR.parent

# Environment

ENV_FILE = "/etc/packagedb/.env"
if not Path(ENV_FILE).exists():
    ENV_FILE = ROOT_DIR / ".env"

env = environ.Env()
environ.Env.read_env(str(ENV_FILE))

# Security

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[".localhost", "127.0.0.1", "[::1]"])

# SECURITY WARNING: do not run with debug turned on in production
DEBUG = env.bool("PACKAGEDB_DEBUG", default=False)

PACKAGEDB_REQUIRE_AUTHENTICATION = env.bool(
    "PACKAGEDB_REQUIRE_AUTHENTICATION", default=False
)

# SECURITY WARNING: do not  run with debug turned on in production
DEBUG_TOOLBAR = env.bool("PACKAGEDB_DEBUG_TOOLBAR", default=False)

PACKAGEDB_PASSWORD_MIN_LENGTH = env.int("PACKAGEDB_PASSWORD_MIN_LENGTH", default=14)

# PackageDB

PACKAGEDB_LOG_LEVEL = env.str("PACKAGEDB_LOG_LEVEL", "INFO")

# Application definition

INSTALLED_APPS = (
    # Local apps
    # Must come before Third-party apps for proper templates override
    'packagedb',
    # Django built-in
    "django.contrib.auth",
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    "django.contrib.humanize",
    # Third-party apps
    'django_filters',
    'rest_framework',
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'packagedbio.urls'

WSGI_APPLICATION = "packagedbio.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": env.str("PACKAGEDB_DB_ENGINE", "django.db.backends.postgresql"),
        "HOST": env.str("PACKAGEDB_DB_HOST", "localhost"),
        "NAME": env.str("PACKAGEDB_DB_NAME", "packagedb"),
        "USER": env.str("PACKAGEDB_DB_USER", "packagedb"),
        "PASSWORD": env.str("PACKAGEDB_DB_PASSWORD", "packagedb"),
        "PORT": env.str("PACKAGEDB_DB_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [str(PROJECT_DIR.joinpath("templates"))],
        "APP_DIRS": True,
        'OPTIONS': {
            "debug": DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                "django.template.context_processors.static",
            ],
        },
    },
]

# Login

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Passwords

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": PACKAGEDB_PASSWORD_MIN_LENGTH,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Testing

# True if running tests through `./manage test or pytest`
IS_TESTS = any(clue in sys.argv for clue in ("test", "pytest"))

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        "LOCATION": "default",
    }
}

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "scanpipe": {
            "handlers": ["null"] if IS_TESTS else ["console"],
            "level": PACKAGEDB_LOG_LEVEL,
            "propagate": False,
        },
        "django": {
            "handlers": ["null"] if IS_TESTS else ["console"],
            "propagate": False,
        },
        # Set PACKAGEDB_LOG_LEVEL=DEBUG to display all SQL queries in the console.
        "django.db.backends": {
            "level": PACKAGEDB_LOG_LEVEL,
        },
    },
}

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_ROOT = env.str("PACKAGEDB_STATIC_ROOT", "./")

STATICFILES_DIRS = [
    str(PROJECT_DIR / "packagedbio" / "static"),
]

# Third-party apps

# Django restframework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    "DEFAULT_PERMISSION_CLASSES": (),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'packagedb.api_custom.PageSizePagination',
    # Limit the load on the Database returning a small number of records by default. https://github.com/nexB/vulnerablecode/issues/819
    "PAGE_SIZE": 10,
}

if not PACKAGEDB_REQUIRE_AUTHENTICATION:
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
        "rest_framework.permissions.AllowAny",
    )

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ("debug_toolbar",)

    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    DEBUG_TOOLBAR_PANELS = (
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    )

    INTERNAL_IPS = [
        "127.0.0.1",
    ]
