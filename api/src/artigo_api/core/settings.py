import os
import environ
import logging

from celery.schedules import crontab

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), '.env')

env = environ.Env(
    DEBUG=(bool, False),
)

try:
    WHERE = env('WHERE')
except:
    WHERE = 'unconfined'

if WHERE in ('prod', 'production'):
    logger.warning('Running in production environment')
elif WHERE == 'testing':
    logger.warning('Running in testing environment')
else:
    logger.warning('Running in development environment')
    environ.Env.read_env(ENV_PATH, overwrite=False)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

try:
    API = env('VUE_APP_API')
    API_URL = f'https://{API}'

    FRONTEND = env('VUE_APP_FRONTEND')
    FRONTEND_URL = f'https://{FRONTEND}'
except:
    API = 'http://localhost:8000'
    API_URL = API

    FRONTEND = 'http://localhost:8080'
    FRONTEND_URL = FRONTEND

logger.warning(f'API URL set to {API_URL}.')

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
    'django_extensions',
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
    'django.middleware.locale.LocaleMiddleware',
    'frontend.middleware.QueryPrintMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ALLOWED_HOSTS = [
    '127.0.0.1',
]

# CSRF_USE_SESSIONS = False
# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SECURE = False

# Should be true in production
# SESSION_COOKIE_SECURE = False

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

try:
    ALLOWED_HOSTS.append(env('VUE_APP_API'))

    CORS_ALLOWED_ORIGINS.extend([
        f'https://{env("VUE_APP_API")}',
        f'https://{env("VUE_APP_FRONTEND")}',
    ])

    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{env("VUE_APP_API")}',
    ])
except:
    ALLOWED_HOSTS.append('localhost')

    CORS_ALLOWED_ORIGINS.extend([
        'http://localhost',
        'http://localhost:8080',
        'http://localhost:8081',
    ])

    CSRF_TRUSTED_ORIGINS.extend([
        'http://localhost',
        'http://localhost:8080',
        'http://localhost:8081',
    ])

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Locales
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

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
            'format': '[{asctime}][{levelname}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
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
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'frontend.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

FORCE_SCRIPT_NAME = '/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = FORCE_SCRIPT_NAME + 'static/'

if DEBUG:
    STATICFILES_DIRS = []

MEDIA_ROOT = os.path.join('/media/')
MEDIA_URL = FORCE_SCRIPT_NAME + 'media/'

GRPC_HOST = env('GRPC_HOST')
GRPC_PORT = env('GRPC_PORT')

IMAGE_EXT = 'jpg'
IMAGE_RESOLUTIONS = [
    # {'max_dim': 200, 'suffix': '_m'},
    {'max_dim': 1080, 'suffix': ''},
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TEST_RUNNER = 'core.runner.PytestTestRunner'

# Celery configuration
CELERY_BROKER_URL = f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/1'
CELERY_RESULT_BACKEND = f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/2'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'export_data': {
        'task': 'core.tasks.export_data',
        'schedule': crontab(day_of_week='*', hour=2, minute=0),
    },
    'renew_cache': {
        'task': 'frontend.tasks.renew_cache',
        'schedule': crontab(hour='*/2', minute=0),
    },
}

# Zenodo configuration
if WHERE in ('prod', 'production'):
    try:
        ZENODO_ACCESS_TOKEN = env('ZENODO_ACCESS_TOKEN')

        CELERY_BEAT_SCHEDULE['upload_data'] = {
            'task': 'core.tasks.upload_data',
            'schedule': crontab(day_of_month='1', hour=5, minute=0),
        }
    except:
        pass

# Custom user model
AUTH_USER_MODEL = 'frontend.CustomUser'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

# Email confirmation
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[ARTigo.org] '
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# After 10 failed login attempts, restrict logins for 30 minutes
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 1800
ACCOUNT_PASSWORD_MIN_LENGTH = 12

# Other settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False

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
        'name': 'Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
        'url': 'https://creativecommons.org/licenses/by-sa/4.0/',
    },
}
