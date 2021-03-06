"""
Django settings for opencanada project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

from os import environ
from os.path import abspath, dirname, join

from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured

_variable_prefix = "OPEN_CANADA_"


def get_env_variable(var_name, default='', required=True):
    try:
        return environ[_variable_prefix + var_name]
    except KeyError:
        if required:
            error_msg = "Set the {} environment variable.".format(_variable_prefix + var_name)
            raise ImproperlyConfigured(error_msg)
        else:
            return default

# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = get_env_variable('BASE_URL')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'compressor',
    'taggit',
    'modelcluster',
    'overextends',

    'core',
    'themes',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    # Overriding wagtailsearch default app registration to register slightly different signal handlers.
    'core.apps.CustomWagtailSearchAppConfig',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtail.contrib.wagtailstyleguide',
    'wagtail.contrib.wagtailroutablepage',

    'favicon',

    'content_notes',
    'interactives',
    'articles',
    'people',
    'images',
    'newsletter',
    'events',
    'jobs',
    'analytics',
    'projects',

    'sitemap',
    'robots',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'opencanada.urls'
WSGI_APPLICATION = 'opencanada.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# SQLite (simplest install)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

# PostgreSQL (Recommended, but requires the psycopg2 library and Postgresql development headers)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'opencanada',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': '',  # Set to empty string for localhost.
#         'PORT': '',  # Set to empty string for default.
#         'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'


# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# COMPRESS_ENABLED = True


# Template configuration


TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'core.context_processors.settings_context',
    'themes.context_processors.default_theme_context',
)


# Wagtail settings

WAGTAIL_SITE_NAME = "opencanada"

# Use Elasticsearch as the search backend for extra performance and better search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/search/backends.html#elasticsearch-backend
#
# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
#         'INDEX': 'opencanada',
#     },
# }

WAGTAILSEARCH_RESULTS_TEMPLATE = 'basic_site/search_results.html'

# Whether to use face/feature detection to improve image cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

FAVICON_PATH = STATIC_URL + 'img/favicon.png'

WAGTAILIMAGES_IMAGE_MODEL = 'images.AttributedImage'

SERVER_EMAIL = "no-reply@opencanada.org"
DEFAULT_FROM_EMAIL = "no-reply@opencanada.org"

try:
    GOOGLE_ANALYTICS_PROPERTY_ID = get_env_variable("GOOGLE_ANALYTICS_PROPERTY_ID")
except ImproperlyConfigured:
    GOOGLE_ANALYTICS_PROPERTY_ID = ''

ANALYTICS_CREDS_PATH = join(PROJECT_ROOT, 'secret')
ANALYTICS_SERVICE_ACCOUNT_EMAIL = get_env_variable("ANALYTICS_SERVICE_ACCOUNT_EMAIL", required=False)

try:
    TWITTER_API_CONSUMER_KEY = get_env_variable("TWITTER_API_CONSUMER_KEY")
except ImproperlyConfigured:
    TWITTER_API_CONSUMER_KEY = ''

try:
    TWITTER_API_CONSUMER_SECRET = get_env_variable("TWITTER_API_CONSUMER_SECRET")
except ImproperlyConfigured:
    TWITTER_API_CONSUMER_SECRET = ''

try:
    TWITTER_API_ACCESS_TOKEN = get_env_variable("TWITTER_API_ACCESS_TOKEN")
except ImproperlyConfigured:
    TWITTER_API_ACCESS_TOKEN = ''

try:
    TWITTER_API_ACCESS_TOKEN_SECRET = get_env_variable("TWITTER_API_ACCESS_TOKEN_SECRET")
except ImproperlyConfigured:
    TWITTER_API_ACCESS_TOKEN_SECRET = ''

try:
    GOOGLE_DEVELOPER_CLIENT_ID = get_env_variable("GOOGLE_DEVELOPER_CLIENT_ID")
except ImproperlyConfigured:
    GOOGLE_DEVELOPER_CLIENT_ID = ''

try:
    GOOGLE_DEVELOPER_CLIENT_SECRET = get_env_variable("GOOGLE_DEVELOPER_CLIENT_SECRET")
except ImproperlyConfigured:
    GOOGLE_DEVELOPER_CLIENT_SECRET = ''

try:
    GOOGLE_DEVELOPER_REFRESH_TOKEN = get_env_variable("GOOGLE_DEVELOPER_REFRESH_TOKEN")
except ImproperlyConfigured:
    GOOGLE_DEVELOPER_REFRESH_TOKEN = ''

try:
    GOOGLE_ANALYTICS_PROFILE_ID = get_env_variable("GOOGLE_ANALYTICS_PROFILE_ID")
except ImproperlyConfigured:
    GOOGLE_ANALYTICS_PROFILE_ID = ''

IS_PRODUCTION = False
ADMIN_ENABLED = True

SITE_ID = 1
