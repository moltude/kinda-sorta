"""
Django settings for kinda_sorta project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

HEROKU = bool(os.environ.get('HEROKU', ''))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if HEROKU:
    DEBUG = False
    TEMPLATE_DEBUG = True
    # get 'local' settings via heroku env
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
    # Parse database configuration from $DATABASE_URL
    # import dj_database_url
    # DATABASES = {'default':  dj_database_url.config()}

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['.herokuapp.com']

    # Static asset configuration
    # STATIC_ROOT = 'static'
    # STATIC_URL = '/static/'

    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'static'),
    # )

if not HEROKU:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = [ '*' ]

    try:
        from .localsettings import *
    except ImportError:
        import sys
        print >> sys.stderr, 'No local settings. Trying to start, but if ' + \
            'stuff blows up, try copying localsettings.py.dist to ' + \
            'localsettings.py and setting appropriately for your environment.'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local app for display
    'beast',
    'django.contrib.humanize',
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



ROOT_URLCONF = 'kinda_sorta.urls'

WSGI_APPLICATION = 'kinda_sorta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'), # static is on root level
    '/Users/scottwilliams/Code/Python/kinda-sorta/site/kinda_sorta',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    # '/Users/scottwilliams/Code/Python/kinda-sorta/site/kinda_sorta',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)


