import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUESTS': True
    }
}

TELEGRAM_APP_ID = "***",
TELEGRAM_API_HASH = "***",
TELEGRAM_BOT_TOKEN = "***"

COINMARKETCAP_API_KEY = "***"

INFURA_KEYS = [
    '***'
]

FINNHUB_API_KEY = "***"
