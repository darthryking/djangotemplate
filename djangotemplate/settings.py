"""
Django settings for djangotemplate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(DIRNAME, ...)
import os
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SETTINGS_DIR, '..')


# Fix for weird x-png MIME types:
import mimetypes
mimetypes.add_type('image/png', '.png', True)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

'''///////////////////////////////////////////////////////////////////
..// Obviously remember to change the SECRET_KEY for each new app! //
.///////////////////////////////////////////////////////////////////'''

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
SECRET_KEY = '[[ INSERT_SECRET_KEY_HERE ]]'

'''///////////////////////////////////////////////////////////////////
..// Obviously remember to change the SECRET_KEY for each new app! //
.///////////////////////////////////////////////////////////////////'''


# SECURITY WARNING: don't run with debug turned on in production!
# Debug variables

# DEBUG = True
# TEMPLATE_DEBUG = True
# NO_SSL = True

DEBUG = False
TEMPLATE_DEBUG = False
NO_SSL = False

SSL_ENABLED = not NO_SSL

if SSL_ENABLED:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    
# Login Redirect URL
LOGIN_URL = 'users_login'


# Not important for debug mode.
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'testapp',
)

MIDDLEWARE_CLASSES = (
    'middleware.ssl.SSLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangotemplate.urls'

WSGI_APPLICATION = 'djangotemplate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, '..', 'database.db'),
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

# Static file collection location
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SETTINGS_DIR, 'static'),
)


# Template Search Paths
TEMPLATE_DIRS = (
    os.path.join(SETTINGS_DIR, 'templates'),
)


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


try:
    """
    In Heroku, the dj_database_url module will exist and so this try block
    will execute successfully. In a non-Heroku environment, the module will
    not exist (unless you installed the Django toolbelt... I think).
    The exception will be caught, and the default settings (as defined above) 
    will not be overridden.
    
    (Added by Ryan)
    
    """
    
    # Parse database configuration from $DATABASE_URL
    import dj_database_url      # <== Our magic bullet
    
    DATABASES['default'] = dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Serve this application under the following host names only
    ALLOWED_HOSTS = ['*']
    
    # Add Gunicorn to installed apps
    INSTALLED_APPS += ('gunicorn',)
    
    
except ImportError:
    pass    # If the import failed, proceed as normal.
    
    