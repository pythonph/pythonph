import os

from django.utils._os import safe_join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['jobs.python.ph', 'localhost']
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'tastypie',
    'api',
    'frontend',
    'registration',
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
ROOT_URLCONF = 'jobs.urls'
WSGI_APPLICATION = 'jobs.wsgi.application'
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
STATIC_URL = '/static/'
STATIC_ROOT = safe_join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    ('lib', safe_join(BASE_DIR, 'bower_components')),
)
TASTYPIE_DEFAULT_FORMATS = ['json']
# django-registration-redux
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = False
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/user/'

try:
    import local_settings
except ImportError:
    pass
