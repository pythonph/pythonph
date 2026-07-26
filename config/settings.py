import os
from pathlib import Path

import django.db.models.signals
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from config.environment import settings

BASE_DIR = Path(__file__).resolve().parent.parent

SENTRY_DSN = os.environ.get("SENTRY_DSN") or getattr(settings, "SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,
        integrations=[
            DjangoIntegration(
                transaction_style="url",
                middleware_spans=True,
                signals_spans=True,
                signals_denylist=[
                    django.db.models.signals.pre_init,
                    django.db.models.signals.post_init,
                ],
                cache_spans=False,
                http_methods_to_capture=("GET",),
            ),
        ],
    )

# ── General Settings ──────────────────────────────────────────────

APP_ENV = settings.APP_ENV
SECRET_KEY = settings.SECRET_KEY
DEBUG = settings.DEBUG

SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

ALLOWED_HOSTS = settings.get_allowed_hosts()
CSRF_TRUSTED_ORIGINS = settings.get_trusted_origins()
CORS_ALLOWED_ORIGINS = settings.get_trusted_origins()

if settings.APP_ENV == "development":
    CORS_ALLOW_ALL_ORIGINS = True

# ── Application definition ────────────────────────────────────────

THIRD_PARTY_APPS = [
    "corsheaders",
    "compressor",
    "taggit",
    "tinymce",
    "ckeditor",
    "markdownx",
    "rest_framework",
]

if settings.APP_ENV == "development":
    THIRD_PARTY_APPS.append("django_browser_reload")

LOCAL_APPS = [
    "app.landing",
    "app.registration",
    "app.jobs",
    "app.slack",
    "app.common",
    "app.organisation",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

if settings.APP_ENV == "development":
    INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")
    INSTALLED_APPS.append("debug_toolbar")

# ── Middleware ─────────────────────────────────────────────────────

LOCAL_MIDDLEWARE = [
    "config.middleware.HealthCheckMiddleware",
]

MIDDLEWARE = (
    [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    + (
        [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]
        if settings.DEBUG
        else []
    )
    + [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
        *LOCAL_MIDDLEWARE,
    ]
)

# ── URL / WSGI / ASGI ─────────────────────────────────────────────

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ── Templates ──────────────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

# ── Database ───────────────────────────────────────────────────────

if settings.APP_ENV == "development":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "DISABLE_SERVER_SIDE_CURSORS": True,
            **settings.get_db_config(),
        }
    }

# ── Cache ──────────────────────────────────────────────────────────

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    }
}

# ── Password validation ────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internationalization ───────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# ── Authentication ─────────────────────────────────────────────────

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "landing"

# ── Static files ───────────────────────────────────────────────────

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MAX_AGE = 86400  # 24 hours

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_URL = "/media/"

# ── Django Compressor ──────────────────────────────────────────────

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG
COMPRESS_OUTPUT_DIR = "cache"

# ── CKEditor ───────────────────────────────────────────────────────

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

# ── REST Framework ─────────────────────────────────────────────────

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
}

# ── Slack ──────────────────────────────────────────────────────────

SLACK_ORG = settings.SLACK_ORG
SLACK_API_TOKEN = settings.SLACK_API_TOKEN
SLACK_BOARD_CHANNEL = settings.SLACK_BOARD_CHANNEL
SLACK_JOBS_CHANNEL = settings.SLACK_JOBS_CHANNEL

# ── Debug Toolbar ──────────────────────────────────────────────────

if settings.DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]

# ── Silenced checks ───────────────────────────────────────────────

SILENCED_SYSTEM_CHECKS = [
    "ckeditor.W001",  # CKEditor 4 EOL — planned migration to TinyMCE
]
