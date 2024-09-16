import ee, os
from decouple import config

DATA_DIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = (
    '127.0.0.1',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'corsheaders',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'povertymappingapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Ensure this is correctly placed
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'povertymappingapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'povertymappingapp.context_processor.variable_settings',
                'cms.context_processors.cms_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'povertymappingapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('kh', 'Khmer')
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

STATIC_ROOT = os.path.join(DATA_DIR, 'static')

GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID')

GOOGLE_OAUTH2_CLIENT_ID = ''

GOOGLE_MAPS_API_KEY = ''


# GEE authentication
# The service account email address authorized by your Google contact.

EE_ACCOUNT =  config('EE_ACCOUNT')
# The private key associated with your service account in Privacy Enhanced
# Email format (deprecated version .pem suffix, new version .json suffix).
EE_PRIVATE_KEY_FILE = os.path.join(BASE_DIR, 'credentials/privatekey.json')
# Service account scope for GEE

GOOGLE_EARTH_SCOPES = ('https://www.googleapis.com/auth/earthengine',)

GOOGLE_OAUTH2_SCOPES = ('https://www.googleapis.com/auth/drive',
                        'profile',
                        'email',
                        )
EE_CREDENTIALS = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)


MAPBOX_API_KEY =  config('MAPBOX_API_KEY')

EE_TASK_POLL_FREQUENCY = 10
# GEE collection
NIGHTLIGHT =  config('NIGHTLIGHT')
WORLDPOP = config('WORLDPOP')
LANDCOVER =  config('LANDCOVER') 
VALNERABILITY_AMD3 =  config('VALNERABILITY_AMD3')

ADM3 =  config('ADM3')
ADM2 =  config('ADM2')
ADM1 =  config('ADM1')
ADM0 =  config('ADM0')

POP_ADM1 =  config('POP_ADM1')
POP_ADM2 =  config('POP_ADM2')
POP_ADM3 =  config('POP_ADM3')
DEPRIVATIONIMG =  config('DEPRIVATIONIMG')
BUILDINGS_POP =  config('BUILDINGS_POP')
BUILDINGS  =  config('BUILDINGS')

IMG_EDUCATION  =  config('IMG_EDUCATION')
IMG_SCHOOL  =  config('IMG_SCHOOL')
IMG_FOOD  =  config('IMG_FOOD')
IMG_HEALTH  =  config('IMG_HEALTH')
IMG_WATER  =  config('IMG_WATER')
IMG_SANITATION  =  config('IMG_SANITATION')
IMG_HANDWASHING  =  config('IMG_HANDWASHING')
IMG_OVERCROWDING  =  config('IMG_OVERCROWDING')
IMG_HOUSING  =  config('IMG_HOUSING')
IMG_FUEL  =  config('IMG_FUEL')
IMG_ELECTRICITY  =  config('IMG_ELECTRICITY')
IMG_ASSETS  =  config('IMG_ASSETS')
IMG_LIVELIHOODBASEDCOPINGSTRATEGIES =  config('IMG_LIVELIHOODBASEDCOPINGSTRATEGIES')
IMG_CONSUMPTION  =  config('IMG_CONSUMPTION')
IMG_TOTALV2  =  config('IMG_TOTALV2')
