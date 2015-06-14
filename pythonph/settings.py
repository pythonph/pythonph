import os

from django.utils._os import safe_join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ['ENV'] == 'DEV'
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['python.ph', 'localhost']

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
    'django_markdown',
    'compressor',
    'raven.contrib.django.raven_compat',
    # pythonph
    'landing',
    'jobs',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pythonph.urls'
WSGI_APPLICATION = 'pythonph.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'NAME': os.environ['POSTGRES_USER'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = safe_join(BASE_DIR, 'static')
MEDIA_ROOT = safe_join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    (
        'skeleton',
        safe_join(BASE_DIR, 'bower_components/skeleton'),
    ),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

TASTYPIE_DEFAULT_FORMATS = ['json']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

if 'SENTRY_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.environ['SENTRY_DSN'],
    }

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
