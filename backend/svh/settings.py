import os


def env_or_def(variable_name, default_value):
    env = os.environ.get(f'DJANGO_{variable_name}')
    if env:
        if env.startswith('[') and env.endswith(']'):
            return [p.replace(' ', '') for p in env.split(',') if p not in ['[',']']]
        if env == 'False':
            return False
        if env == 'True':
            return True
    return env or default_value

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_or_def('SECRET_KEY','7iucc&h6dmmyne=7fih(*b-y(oy^x&+13nsv=10nz@hyp-2*_g')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_or_def('DEBUG', True)

ALLOWED_HOSTS = env_or_def('ALLOWED_HOSTS', '*')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'svh',
    'rest_framework',
    'rest_framework_swagger',
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

ROOT_URLCONF = 'svh.urls'

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
                'svh.utils.common_context_variables'
            ],
        },
    },
]


WSGI_APPLICATION = 'svh.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'svh',
        'USER': 'svh',
        'HOST': 'localhost',
    },
}

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-en'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = env_or_def('MEDIA_URL', '/media/')
MEDIA_ROOT = env_or_def('MEDIA_ROOT', '/media/')


# SVH settings
PREVIEW_HEIGHT = 200
DESCRIPTION_FILENAME = 'description.yaml'
MAX_THREADS_REACTOR = 5
ALLOW_SOURCE_SERVING = True
METRICS_SCRIPT = '' # override this in local settings with Yandex.Metrika or whatever

CELERY_BROKER_URL = 'amqp://rabbit'

TORRENT_SERVICE_URL = 'http://torrent:8080'

# File service settings
FILESERVICE_URL = 'http://localhost:5000'
FILESERVICE_SOURCES_FOLDER = 'sources/'

SOURCE_VIDEOS_PATH = os.path.join(MEDIA_ROOT, 'sources')

RABBIT_SETTINGS = {
    "Host": env_or_def('RABBIT_HOST',"localhost"),
    "UserName": "guest",
    "Password": "guest",
    "Port": 5672,
    "VirtualHost": "/",
    "RabbitEndpoints":
    {
      "Tasks": {
        "Exchange": "svh.tasks.v1",
        "ExchangeType": "fanout",
        "Queue": "svh.tasks.v1.backend.queue",
        "RoutingKey": "*"
      },
      "Events": {
        "Exchange": "svh.events.v1",
        "ExchangeType": "fanout",
        "Queue": "svh.events.v1.backend.queue",
        "RoutingKey": "*"
      }
    }
  }

REST_FRAMEWORK = {

'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}