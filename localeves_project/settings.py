# File: localeves_project/settings.py

from pathlib import Path
from decouple import config

# BASE_DIR is the absolute path to your project root
# Path(__file__) is the path to this settings.py file itself
# .resolve() converts it to an absolute path
# .parent gives the localeves_project/ folder
# .parent again gives the project root (LocalEve/)
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security Settings ---
# Both loaded from .env via python-decouple
# Never hardcode these — they must never appear in Git
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

# Hosts that are allowed to make requests to this server
# In development: only localhost
# In production: add your actual domain here
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# --- Installed Apps ---
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Local
    'accounts',
    'establishments',
    'map',
    'chat',
]

LOGIN_URL = 'account_login'
# Must be set before any migrations are run
AUTH_USER_MODEL = 'accounts.CustomUser'

# Required by allauth's sites framework integration
SITE_ID = 1

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'localeves_project.urls'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'localeves_project.wsgi.application'

# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# --- ASGI Application ---
ASGI_APPLICATION = 'localeves_project.asgi.application'


# --- Channel Layers ---
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
           
        },
    },
}


# --- Authentication ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- allauth Configuration ---
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = '/map/'
LOGOUT_REDIRECT_URL = '/'
# Note: No ACCOUNT_LOGOUT_ON_GET here — we keep the default
# secure behaviour which requires POST for logout

# --- Email ---
# Development only — prints emails to terminal
# Production: swap for SMTP backend + credentials in .env
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalisation ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# --- Media Files ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Misc ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'