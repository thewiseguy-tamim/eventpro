import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Core
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-unsafe-key')
DEBUG = False

ALLOWED_HOSTS = ['*', '.vercel.app']

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://*.onrender.com',
]

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Optional: Cloudinary
    'cloudinary',
    'cloudinary_storage',

    # Your apps
    'event',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# Database
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        default='postgresql://postgres.endwqrkxnxcvozpwueik:Tamim%40%401900@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres',
        conn_max_age=0,
        ssl_require=True,
    )
}
CONN_HEALTH_CHECKS = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# I18N
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static (WhiteNoise)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # keep if you have a /static dir
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media
MEDIA_URL = '/media/'
# Always set MEDIA_ROOT to your real media folder (matches your repo layout)
MEDIA_ROOT = BASE_DIR / 'media'

# Use Cloudinary only in non-debug AND when creds exist
cloudinary_creds_present = (
    os.getenv('CLOUDINARY_URL')
    or (
        os.getenv('CLOUDINARY_CLOUD_NAME')
        and os.getenv('CLOUDINARY_API_KEY')
        and os.getenv('CLOUDINARY_API_SECRET')
    )
)
use_cloudinary = (not DEBUG) and bool(cloudinary_creds_present)

if use_cloudinary:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
        'SECURE': True,
    }
    try:
        import cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=CLOUDINARY_STORAGE['API_KEY'],
            api_secret=CLOUDINARY_STORAGE['API_SECRET'],
            secure=True,
        )
    except Exception:
        pass

    STORAGES = {
        'default': {'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    }
else:
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    }

# Misc
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# Email (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')