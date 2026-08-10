import os
from pathlib import Path

import django.db.models.signals
import sentry_sdk
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
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
    "django_tailwind_cli",
    "taggit",
    "tinymce",
    "import_export",
    "rest_framework",
]

if settings.APP_ENV == "development" and settings.DEBUG:
    THIRD_PARTY_APPS.append("django_browser_reload")

LOCAL_APPS = [
    "app.accounts",
    "app.landing",
    "app.jobs",
    "app.events",
    "app.organisation",
]

UNFOLD_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
]

INSTALLED_APPS = [
    *UNFOLD_APPS,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Required by FORM_RENDERER = TemplatesSetting so built-in widget
    # templates (django/forms/widgets/*) resolve from this app's dir.
    "django.forms",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

if settings.DEBUG:
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
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        ]
        if settings.APP_ENV == "development" and settings.DEBUG
        else []
    )
    + [*LOCAL_MIDDLEWARE]
)

# ── URL / WSGI / ASGI ─────────────────────────────────────────────

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ── Templates ──────────────────────────────────────────────────────

# Render form widgets through the main TEMPLATES engine so project-level
# overrides (e.g. templates/auth/widgets/) are picked up; the default
# ``DjangoTemplates`` form renderer only searches app template dirs.
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

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
                "app.landing.context_processors.site_settings",
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

LOGIN_URL = "landing:login"
LOGIN_REDIRECT_URL = "landing:landing"
LOGOUT_REDIRECT_URL = "landing:landing"

AUTHENTICATION_BACKENDS = [
    "app.landing.backends.EmailBackend",
]

# ── Static files ───────────────────────────────────────────────────

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

STATICFILES_DIRS = [
    STATIC_DIR,
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

WHITENOISE_MAX_AGE = 86400  # 24 hours

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_URL = "/media/"

# ── Storage ────────────────────────────────────────────────────────
# Uploaded media goes to Cloudflare R2 (S3-compatible) when credentials are
# configured; otherwise it falls back to the local filesystem (MEDIA_ROOT).
# Static files always stay on WhiteNoise.

if settings.use_r2():
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.StaticFilesStorage",
        },
    }

    AWS_ACCESS_KEY_ID = settings.R2_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.R2_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = settings.R2_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    AWS_S3_REGION_NAME = "auto"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_QUERYSTRING_AUTH = False  # public bucket — no signed URLs
    AWS_DEFAULT_ACL = None  # R2 does not support object ACLs
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    if settings.R2_PUBLIC_URL:
        AWS_S3_CUSTOM_DOMAIN = settings.R2_PUBLIC_URL
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.StaticFilesStorage",
        },
    }

# ── Tailwind CLI ───────────────────────────────────────────────────

TAILWIND_CLI_SRC_CSS = "src/styles/main.css"
TAILWIND_CLI_DIST_CSS = "css/app.css"
TAILWIND_CLI_USE_DAISY_UI = True

# ── TinyMCE ───────────────────────────────────────────────────────

TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "license_key": "gpl",
    "branding": False,
    "promotion": False,
    "menubar": "file edit view insert format tools table help",
    "plugins": (
        "advlist autolink lists link image charmap preview anchor "
        "searchreplace visualblocks code fullscreen insertdatetime media "
        "table help wordcount"
    ),
    "toolbar": (
        "undo redo | blocks | bold italic underline | "
        "alignleft aligncenter alignright alignjustify | "
        "bullist numlist outdent indent | link image media table | "
        "removeformat | code fullscreen"
    ),
}

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

# ── Debug Toolbar ──────────────────────────────────────────────────

if settings.DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]

# ── Django Unfold (Admin) ──────────────────────────────────────────


def unfold_environment_callback(request):
    """Return a label and variant for the environment shown in the admin header."""
    if APP_ENV == "production":
        return ["Production", "danger"]
    if APP_ENV == "staging":
        return ["Staging", "warning"]
    return ["Development", "info"]


UNFOLD = {
    "SITE_TITLE": "PythonPH Admin",
    "SITE_HEADER": "PythonPH",
    "SITE_SUBHEADER": "Admin",
    "SITE_SYMBOL": "rocket_launch",
    "ENVIRONMENT": unfold_environment_callback,
    "BORDER_RADIUS": "6px",
    "STYLES": [
        lambda request: static("css/tinymce-theme.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/tinymce-theme.js"),
    ],
    "COLORS": {
        "base": {
            "50": "#f2f4fb",
            "100": "#e6e9f7",
            "200": "#c9d0ee",
            "300": "#a2b0e0",
            "400": "#6f83c9",
            "500": "#4a5dab",
            "600": "#35467f",
            "700": "#273460",
            "800": "#1b254a",
            "900": "#101c42",
            "950": "#0a122b",
        },
        "primary": {
            "50": "#fffdf0",
            "100": "#fef9d8",
            "200": "#fdf1a8",
            "300": "#fde876",
            "400": "#fdde50",
            "500": "#fdd649",
            "600": "#e0b41f",
            "700": "#b88e14",
            "800": "#8f6a0e",
            "900": "#6b4d09",
            "950": "#453005",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },
    "LOGIN": {
        "image": lambda request: static("img/login-bg.svg"),
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Sections"),
                        "icon": "category",
                        "link": reverse_lazy("admin:landing_section_changelist"),
                    },
                    {
                        "title": _("Events"),
                        "icon": "event",
                        "link": reverse_lazy("admin:events_event_changelist"),
                    },
                ],
            },
            {
                "title": _("Jobs"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Companies"),
                        "icon": "business",
                        "link": reverse_lazy("admin:jobs_company_changelist"),
                    },
                    {
                        "title": _("Job posts"),
                        "icon": "work",
                        "link": reverse_lazy("admin:jobs_job_changelist"),
                    },
                ],
            },
            {
                "title": _("Users"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Committees"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:organisation_commitee_changelist"),
                    },
                    {
                        "title": _("Volunteers"),
                        "icon": "volunteer_activism",
                        "link": reverse_lazy("admin:organisation_volunteer_changelist"),
                    },
                ],
            },
        ],
    },
}
