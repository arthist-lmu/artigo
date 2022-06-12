'''
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
'''

import os
import environ

from datetime import timedelta

# Use django-environ config
env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

FORCE_SCRIPT_NAME = '/'

try:
    API = env('DOMAIN')
    API_URL = 'https://' + API
except:
    API = 'http://localhost:8000'
    API_URL = 'http://localhost:8000'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'dj_rest_auth',
    'corsheaders',
    'frontend',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'frontend.middleware.QueryPrintMiddleware',
]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:8081',
]

# CSRF_USE_SESSIONS = False
# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SECURE = False

# Should be true in production
# SESSION_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:8081',
]

try:
    ALLOWED_HOSTS.append(env('DOMAIN'))
    CORS_ALLOWED_ORIGINS.extend([
        f'https://{env("DOMAIN")}',
        f'https://{env("FRONTEND_DOMAIN")}',
    ])
    CSRF_TRUSTED_ORIGINS.append(f'https://{env("DOMAIN")}')
except:
    pass

ROOT_URLCONF = 'core.urls'

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
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'core.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': f'{env("MEMCACHED_HOST")}:{env("MEMCACHED_PORT")}',
        'TIMEOUT': 60 * 60 * 24,
    }
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname}: {message}',
            'style': '{',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'frontend.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_DIRS = []

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = FORCE_SCRIPT_NAME + 'static/'

MEDIA_ROOT = os.path.join('/media/')
MEDIA_URL = FORCE_SCRIPT_NAME + 'media/'

GRPC_HOST = env('GRPC_HOST')
GRPC_PORT = env('GRPC_PORT')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TEST_RUNNER = 'core.runner.PytestTestRunner'

# Celery configuration
CELERY_BROKER_URL = f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/1'
CELERY_RESULT_BACKEND = f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/2'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'export_jsonl': {
        'task': 'core.tasks.export_jsonl',
        'schedule': timedelta(hours=12),
    },
    'renew_cache': {
        'task': 'frontend.tasks.renew_cache',
        'schedule': timedelta(hours=1),
    },
}

# Custom user model
AUTH_USER_MODEL = 'frontend.CustomUser'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

# Email confirmation
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Artigo.org]'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# After 10 failed login attempts, restrict logins for 30 minutes
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 1800
ACCOUNT_PASSWORD_MIN_LENGTH = 12

# Other settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# TODO: change to mandatory
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
SOCIALACCOUNT_AUTO_SIGNUP = False

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        },
    },
    'google': {
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

SPECTACULAR_SETTINGS = {
    'TITLE': 'ARTigo',
    'DESCRIPTION': 'Social Image Tagging',
    'VERSION': '1.0.0',
    'CONTACT': {
        'email': 'feedback@artigo.org',
    },
    'LICENSE': {
        'name': 'GNU General Public License v3.0',
        'url': 'https://github.com/arthist-lmu/artigo/blob/master/LICENSE.md',
    },
    'PREPROCESSING_HOOKS': [
        'frontend.utils.urls.preprocessing_hook',
    ],
}
