import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '-1')
GENERAL_URL = os.getenv('GENERAL_URL', 'https://example.com')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '158.160.58.44',
    '127.0.0.1',
    'localhost',
    'pb.vvvas.ru',
]

CSRF_TRUSTED_ORIGINS = ['https://pb.vvvas.ru']
# CSRF_TRUSTED_ORIGINS = [GENERAL_URL]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_reorder',
    'rangefilter',
    'import_export',
    'bot.apps.BotConfig',
    'users.apps.UsersConfig',
    'realties.apps.RealtiesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'realty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
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

WSGI_APPLICATION = 'realty.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432)
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/bstatic/'
STATIC_ROOT = '/app/static/bstatic/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

IMPORT_EXPORT_USE_TRANSACTIONS = True

ADMIN_REORDER = (
    {
        'app': 'realties',
        'label': 'Недвижимость и объявления ',
        'models': (
            'realties.Realty',
            'realties.Ad',
            'realties.Category',
            'realties.City',
        )
    },
    {
        'app': 'realties',
        'label': 'Комментарии пользователей',
        'models': (
            'realties.Comment',
            'realties.Photo'
        )
    },
    {
        'app': 'bot',
    },
    {
        'app': 'users',
        'models': (
            'users.User',
            'users.Profile'
        )
    },
)

# JAZZMIN_SETTINGS = {
#     "show_sidebar": False,
#     "topmenu_links": [
#         {"name": "Главная",  "url": "admin:index", "permissions": ["auth.view_user"]},
#     ],
# }
# JAZZMIN_SETTINGS["show_ui_builder"] = True

ADMIN_PERMISSIONS = [
    'change_profile',
    'view_profile',
    'add_ad',
    'change_ad',
    'view_ad',
    'add_category',
    'change_category',
    'view_category',
    'add_city',
    'change_city',
    'view_city',
    'add_comment',
    'change_comment',
    'view_comment',
    'add_realty',
    'change_realty',
    'view_realty',
    'add_photo',
    'change_photo',
    'view_photo',
]
