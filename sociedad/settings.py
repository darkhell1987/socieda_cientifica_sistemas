"""
Django settings for sociedad project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9*v7ducii4a1v!0(q!pqm*i!st$4s!m)=-i7(!whtu7b(pmk#7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sociedad.apps.principal',
    'sociedad.apps.blog',
    'sociedad.apps.biblioteca',
    'sociedad.apps.noticias',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sociedad.urls'

WSGI_APPLICATION = 'sociedad.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sis_db',
        'USER' : 'root',
        'PASSWORD' : '',
        'HOST' : '',
        'PORT' : '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-Bo'

TIME_ZONE = 'America/Bolivia'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

RUTA_PROYECTO = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DIRS = (
    os.path.join(RUTA_PROYECTO,'plantillas'),
    )
STATICFILES_DIRS = (
    os.path.join(RUTA_PROYECTO,'static'),
    )
MEDIA_ROOT = os.path.join(RUTA_PROYECTO,'carga')

MEDIA_URL = '/archivos/'

AUTH_PROFILE_MODULE = "principal.perfil"