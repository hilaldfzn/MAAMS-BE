"""
Django settings for maams_be project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path


# Setup environment variables.
# Production & staging environment variables will be stored on Dockerfile
# and will be populated through pipeline using CI/CD variables as args.
import os
from dotenv import load_dotenv, find_dotenv
from django.core.exceptions import ImproperlyConfigured

# Load current environment if .env file exists
env_file = find_dotenv(
     filename=".env",
     raise_error_if_not_found=False,
     usecwd=False
)
if env_file:
    load_dotenv(env_file, verbose=True)
active_env = str(os.environ["ENVIRONMENT"])
# If a new environment is added,
# check here to load .env file if file is present.
if active_env == 'DEVELOPMENT':
        load_dotenv('./.env.dev')
 
def get_env_value(env_variable: str) -> str | int | bool | None:
    """
    Gets environment variables depending on active environment.
    """
    try:
        value = parse_env_value(os.environ[env_variable])
        return value
    except KeyError:
        error_msg = f'{env_variable} environment variable not set.'
        raise ImproperlyConfigured(error_msg)

def parse_env_value(value: str) -> str | bool | int | None:
    """
    Parses environment variable into either bool, strings, ints, or None type.
    """
    value = value.lower()
    if value == "none": return None             # Checks for None type
    if value in ["0", "false"]: return False    # Checks for bool types
    if value in ["1", "true"]: return True
    if value.isnumeric(): return int(value)     # Checks for int types
    # Return string if none of the above type matches
    return value                                


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_value("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_value("DEBUG")

ALLOWED_HOSTS = get_env_value("ALLOWED_HOSTS").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'validator',
]

# Django REST Framework configurations
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DRF-Spectacular configurations, OpenAPI3 schema generator
SPECTACULAR_SETTINGS = {
    'TITLE': 'MAAMS-BE',
    'DESCRIPTION': 'Backend API documentation for MAAMS.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

ROOT_URLCONF = 'maams_be.urls'

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

WSGI_APPLICATION = 'maams_be.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_value("DB_NAME"),
        'USER': get_env_value("DB_USER"),
        'PASSWORD': get_env_value("DB_PASSWORD"),
        'HOST': get_env_value("DB_HOST"),
        'PORT': get_env_value("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
