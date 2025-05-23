from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-vsov8t#zh^%%jlmwvm5qubiu8y-&ci(2c$=iht_cf8j95%t64%'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

# Celery
CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/0"
CELERY_RESULT_BACKEND = f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/0"

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'