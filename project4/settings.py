"""
Django settings for project4 project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

########################################
#                                      #
#       GLOBAL SETTING VARS            #
#                                      #
########################################
PAGINATION_POST_COUNT = 10





# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '13kl@xtukpwe&xj2xoysxe9_6=tf@f8ewxer5n&ifnd46+6$%8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'touiteur-app.herokuapp.com'
]


# Application definition

INSTALLED_APPS = [
    'network',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage', #custom
    # 'debug_toolbar', #custom
    'sorl.thumbnail', #custom
    'cloudinary', #custom
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # this is custom! Needs to be after SessionMiddleware, but before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Custom Localization middleware
    # Overrides other localization settings such as browser locale, and instead sets it based on a field in the user model, if available
    # Needs to be after AuthentificationMiddleware because that creates the user object
    'network.middleware.translation_middleware.UserPrefLocaleMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', # this is custom! Should be the last middleware to load unless there's a very good reason to load something else later
]

ROOT_URLCONF = 'project4.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'network', 'templates'),
        ],
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

WSGI_APPLICATION = 'project4.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        # to anyone reading this code: i'm aware that it's not good practice to put
        # DB credentials in plain text. however this is just for test deployment to a
        # heroku container that will be deleted after initial testing. no real user
        # information will ever be in the database.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ddhn0srsct6ho6',
        'USER': 'tvtnqnautyvsvy',
        'PASSWORD': 'd9a6334671f4a6c329dae7d6f6e6cf931e77fbcdefecd68bc0bba69af55bb827',
        'HOST': 'ec2-52-214-178-113.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}


AUTH_USER_MODEL = "network.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
    ('ja', 'Japanese'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'network', 'locale'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
django_heroku.settings(locals())

# where our uploaded files are located on the filesystem
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# url to access our uploaded files
MEDIA_URL = '/media/'

# internal IPs for debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]
# COUDINARY_STORAGE = {
#     'CLOUD_NAME': 'hptitepok',
#     'API_KEY': '',
#     'API_SECRET': '',
# }
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'