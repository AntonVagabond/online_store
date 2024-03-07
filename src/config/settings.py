import os
from datetime import timedelta

import environ
import sentry_sdk
from celery.schedules import crontab

root = environ.Path(__file__)
env = environ.Env()
environ.Env.read_env(env.str(root(), default='.env'))

BASE_DIR = root()

SECRET_KEY = env.str(var='SECRET_KEY')
DEBUG = env.bool(var='DEBUG', default=False)
ALLOWED_HOSTS = env.str(var='ALLOWED_HOSTS', default='').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # packages
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'djoser',
    'phonenumber_field',
    'debug_toolbar',
    # apps
    'api',
    'common',
    'users',
    'products',
    'carts',
    'delivers',
    'orders',
    'payments',
    # after apps
    'drf_spectacular',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # package middlewares
    'corsheaders.middleware.CorsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'request_logging.middleware.LoggingMiddleware',
    # 'customers.middleware.ActiveUserMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# region -------------------------- DATABASE ----------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str(var='PG_DATABASE', default='postgres'),
        'USER': env.str(var='PG_USER', default='postgres'),
        'PASSWORD': env.str(var='PG_PASSWORD', default='postgres'),
        'HOST': env.str(var='DB_HOST', default='localhost'),
        'PORT': env.int(var='DB_PORT', default=5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# endregion -------------------------------------------------------------------------

# region --------------------- DJANGO REST FRAMEWORK --------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATED_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
}
# endregion -------------------------------------------------------------------------

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

# region --------------------------- LOCALIZATION -----------------------------------
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
# endregion -------------------------------------------------------------------------

# region ------------------------- STATIC AND MEDIA ---------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media/test/')
# endregion -------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# region --------------------------- CORS HEADERS -----------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False
# endregion -------------------------------------------------------------------------

# region ------------------------ DRF SPECTACULAR -----------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Online Store',
    'DESCRIPTION': 'Online Store',
    'VERSION': '1.0.0',

    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.BasicAuthentication'
    ],

    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': True,
        'syntaxHighlight.active': True,
        'syntaxHighlight.theme': 'arta',
        'defaultModelsExpandDepth': -1,
        'displayRequestDuration': True,
        'filter': True,
        'requestSnippetsEnabled': True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}
# endregion -------------------------------------------------------------------------


# region ------------------------------ SMTP ----------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Настройка почтового сервера по SMTP-протоколу
EMAIL_HOST = env.str(var='EMAIL_HOST')
EMAIL_PORT = env.int(var='EMAIL_PORT')
EMAIL_USE_TLS = env.bool(var='EMAIL_USE_TLS')
EMAIL_HOST_USER = env.str(var='EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str(var='EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER
# endregion -------------------------------------------------------------------------


# region ----------------------- DJOSER AND SIMPLE JWT-------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'users.serializers.api.users.RegistrationSerializer',
        'user': 'users.serializers.api.users.UserSerializer',
        'current_user': 'users.serializers.api.users.UserSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
}
# endregion -------------------------------------------------------------------------

# region ------------------ CUSTOM USER, CUSTOM BACKEND -----------------------------
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('users.backends.AuthBackend',)
# endregion -------------------------------------------------------------------------

# region ------------------------------- REDIS --------------------------------------
REDIS_URL = env.str(var='REDIS_URL', default='redis://localhost:6379/0')
# Кэш с помощью => Redis.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}
# endregion -------------------------------------------------------------------------

# region ----------------------------- RABBITMQ -------------------------------------
RABBIT_URL = env.str(var='RABBITMQ_URL', default='amqp://guest:guest@localhost:5672')
# endregion -------------------------------------------------------------------------

# region ------------------------------- CELERY -------------------------------------
# Использование брокера сообщений для Celery на базе RabbitMQ.
CELERY_BROKER_URL = RABBIT_URL
# Использование БД для Celery на базе Redis.
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_TRACK_STARTED = env.bool(var='CELERY_TASK_TRACK_STARTED', default=False)
CELERY_TASK_TIME_LIMIT = 30 * 60
accept_content = [env.str(var='ACCEPT_CONTENT', default='application/json')]
result_serializer = env.str(var='RESULT_SERIALIZER', default='json')
task_serializer = env.str(var='TASK_SERIALIZER', default='json')
timezone = env.str(var='TIMEZONE', default='Europe/Moscow')

# Резервная копия Базы Данных с помощью => Celery Beat.
CELERY_BEAT_SCHEDULE = {
    'backup_database': {
        # Путь к задаче указанной в tasks.py.
        'task': 'common.tasks.db_backup_task',
        # Резервная копия будет создаваться каждый день в полночь.
        'schedule': crontab(hour='0', minute='0'),
    },
}
# endregion -------------------------------------------------------------------------

# region ------------------------------ YOOKASSA ------------------------------------
YOOKASSA_SHOP_ID = env.int(var='YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = env.str(var='YOOKASSA_SECRET_KEY')
YOOKASSA_RETURN_URL = env.str(var='YOOKASSA_RETURN_URL')
# endregion -------------------------------------------------------------------------


# region ------------------------- DJANGO DEBUGGER ----------------------------------
if DEBUG:
    # region ------------------------- SENTRY ---------------------------------------
    sentry_sdk.init(
        dsn=env.str(var='SENTRY_DSN', default=''),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
    # endregion ---------------------------------------------------------------------

    INTERNAL_IPS = [
        '127.0.0.1',
    ]
# endregion -------------------------------------------------------------------------


# region ------------------------------- LOGGING ------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'logstash': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(message)s',
            'json_indent': None,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logstash': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 50000,  # Значение по умолчанию: 5959
            'version': 1,
            'message_type': 'django',
            'fqdn': False,  # Полное доменное имя. Значение по умолчанию: false.
            'tags': ['django.request'],  # Список тегов. По умолчанию: None.
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'request_logging': {
            'handlers': ['console', 'logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
# endregion -------------------------------------------------------------------------
