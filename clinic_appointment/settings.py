"""
Django settings for clinic_appointment project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── SECURITY ───────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-o_dyoxq6&nkkp%*qj9@zp-6+w8@f^_(5@$swwbtl^5&%c@b1xp')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*', '.onrender.com', 'localhost', '127.0.0.1']


# ─── APPS ───────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Our apps
    'patients',
    'appointments',
    'analytics',
    'accounts',
]

# ─── MIDDLEWARE ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← Render sathi zaruree
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clinic_appointment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clinic_appointment.wsgi.application'


# ─── DATABASE ───────────────────────────────────────────────
# Render var DATABASE_URL environment variable asel
# Local var PostgreSQL use hote

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Render / Production
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local Development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'clinic_db',
            'USER': 'postgres',
            'PASSWORD': 'Indrajit@7397',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# ─── PASSWORD VALIDATION ────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── INTERNATIONALIZATION ───────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ─── STATIC FILES ───────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   # ← collectstatic sathi
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ─── AUTH / LOGIN ───────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/login/'


# ─── SESSION SECURITY ───────────────────────────────────────
SESSION_COOKIE_AGE = 1209600       # 2 weeks
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG  # Production la auto True


# ─── EMAIL ──────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'tumcha_email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tumcha_app_password')
DEFAULT_FROM_EMAIL = f'Clinic Dashboard <{EMAIL_HOST_USER}>'


# ─── LOGIN SECURITY ─────────────────────────────────────────
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15


# ─── DEFAULT PRIMARY KEY ────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'