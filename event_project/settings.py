import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env locally (Vercel uses its own env store)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Secrets from environment
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-unsafe-key')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['*', '.vercel.app']

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'http://127.0.0.1:8000',
    'https://*.onrender.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'event',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_project.urls'

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

WSGI_APPLICATION = 'event_project.wsgi.application'

# Database (Supabase). Use transaction pooler (6543) and no persistent connections (serverless-safe)
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        default='postgresql://postgres.endwqrkxnxcvozpwueik:Tamim%40%401900@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres',
        conn_max_age=0,
        ssl_require=True,
    )
}
CONN_HEALTH_CHECKS = True

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (use Cloudinary on Vercel; fallback to /tmp if not configured)
MEDIA_URL = '/media/'

use_cloudinary = bool(
    os.getenv('CLOUDINARY_URL') or (
        os.getenv('CLOUDINARY_CLOUD_NAME')
        and os.getenv('CLOUDINARY_API_KEY')
        and os.getenv('CLOUDINARY_API_SECRET')
    )
)

if use_cloudinary:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }
    default_storage_backend = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Temporary local storage to avoid 500s on Vercel (files won't persist)
    default_storage_backend = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = '/tmp/media'

# Django 5+ storage settings
STORAGES = {
    'default': {
        'BACKEND': default_storage_backend,
    },
    'staticfiles': {
        # Use non-manifest storage to avoid startup crash if collectstatic isn't run
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Email settings (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')