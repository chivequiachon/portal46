"""
Django settings for portal46 project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku 
import django_redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a+3m^f_$@wdw#(vql-=$5z3dni4&@1*o1jo5de(isxd-y8r^wb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG']

if DEBUG is not None:
  if DEBUG == '1':
    DEBUG = True
  else:
    DEBUG = False
else:
  DEBUG = False

CURRENT_HOST = os.environ['CURRENT_HOST']
ALLOWED_HOSTS = [CURRENT_HOST]


# Application definition

INSTALLED_APPS = [
    'portal',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal46.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'portal46.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEVELOP_DB    = {'HOST':'127.0.0.1', 'NAME':'portal46',       'USER':'portal46user', 'PASSWORD':'GatewAy1011'}
STAGING_DB    = {'HOST':'ec2-54-225-230-142.compute-1.amazonaws.com', 'NAME':'d17k9bjlejeh5b', 'USER':'xkmkmtvxqgsynt', 'PASSWORD':'e5b18aeb9ad2edcb7e43534d28d8a160b612192ddda63e926582ef5945af1b71'}
PRODUCTION_DB = {'HOST':'ec2-23-23-93-115.compute-1.amazonaws.com', 'NAME':'df6nimjp6v0q7d', 'USER':'gwloobrusszhtn', 'PASSWORD':'d9c3849f8f5f6a0471d9b75ab7e244b1b59f456ab0e34b40f71af4a18c9bf373'}

DB_SETTINGS = None
MACHINE = os.environ['MACHINE']
if MACHINE == 'DEVELOP':
    DB_SETTINGS = DEVELOP_DB
elif MACHINE == 'STAGING':
    DB_SETTINGS = STAGING_DB
elif MACHINE == 'PRODUCTION':
    DB_SETTINGS = PRODUCTION_DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_SETTINGS['NAME'],
        'USER': DB_SETTINGS['USER'],
        'PASSWORD': DB_SETTINGS['PASSWORD'],
        'HOST': DB_SETTINGS['HOST'],
        'PORT': '5432',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis-12889.c17.us-east-1-4.ec2.cloud.redislabs.com:12889/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "GatewAy1011"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

django_heroku.settings(locals())
