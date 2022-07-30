import os

from django.utils._os import safe_join

import dj_database_url
import environ

env = environ.Env(
    SECRET_KEY=(str, 'devkey'),
    ENV=(str, 'DEV'),
    DATABASE_URL=(str, 'sqlite:///db.sqlite3'),
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('ENV') == 'DEV'
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['python.ph', 'localhost', '*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'taggit',
    'tastypie',
    'compressor',
    'raven.contrib.django.raven_compat',
    'markdownx',
    'adminsortable2',
    'ckeditor',
    # pythonph
    'landing',
    'registration',
    'jobs',
    'slack',
    'common',
)
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Keep this here as stated on docs
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pythonph.urls'
WSGI_APPLICATION = 'pythonph.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL')),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = safe_join(BASE_DIR, 'static')
MEDIA_ROOT = safe_join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "landing"

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

TASTYPIE_DEFAULT_FORMATS = ['json']

SENTRY_DSN = env('SENTRY_DSN', default=None)

if SENTRY_DSN:
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

SLACK_ORG = env('SLACK_ORG', default=None)
SLACK_API_TOKEN = env('SLACK_API_TOKEN', default=None)
SLACK_BOARD_CHANNEL = env('SLACK_BOARD_CHANNEL', default=None)
SLACK_JOBS_CHANNEL = env('SLACK_JOBS_CHANNEL', default=None)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
              ],
         },
    },
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
