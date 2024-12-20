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
VALNERABILITY_AMD3_19 =  config('VULNERABILITY_AMD3_19')
VALNERABILITY_AMD3_22 =  config('VULNERABILITY_AMD3_22')
VALNERABILITY_AMD3_23 =  config('VULNERABILITY_AMD3_23')

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

# 2019
IMG_EDUCATION19  =  config('IMG_EDUCATION19')
IMG_FOOD19  =  config('IMG_FOOD19')
IMG_HEALTH19  =  config('IMG_HEALTH19')
IMG_WATER19  =  config('IMG_WATER19')
IMG_SANITATION19  =  config('IMG_SANITATION19')
IMG_HANDWASHING19  =  config('IMG_HANDWASHING19')
IMG_OVERCROWDING19  =  config('IMG_OVERCROWDING19')
IMG_HOUSING19  =  config('IMG_HOUSING19')
IMG_FUEL19  =  config('IMG_FUEL19')
IMG_ELECTRICITY19  =  config('IMG_ELECTRICITY19')
IMG_ASSETS19  =  config('IMG_ASSETS19')
IMG_LIVELIHOODBASEDCOPINGSTRATEGIES19 =  config('IMG_LIVELIHOODBASEDCOPINGSTRATEGIES19')
IMG_CONSUMPTION19  =  config('IMG_CONSUMPTION19')
IMG_TOTALV219  =  config('IMG_TOTALV219')

# 2022
IMG_EDUCATION22  =  config('IMG_EDUCATION22')
IMG_FOOD22  =  config('IMG_FOOD22')
IMG_HEALTH22  =  config('IMG_HEALTH22')
IMG_WATER22  =  config('IMG_WATER22')
IMG_SANITATION22  =  config('IMG_SANITATION22')
IMG_HANDWASHING22  =  config('IMG_HANDWASHING22')
IMG_OVERCROWDING22  =  config('IMG_OVERCROWDING22')
IMG_HOUSING22  =  config('IMG_HOUSING22')
IMG_FUEL22  =  config('IMG_FUEL22')
IMG_ELECTRICITY22  =  config('IMG_ELECTRICITY22')
IMG_ASSETS22  =  config('IMG_ASSETS22')
IMG_LIVELIHOODBASEDCOPINGSTRATEGIES22 =  config('IMG_LIVELIHOODBASEDCOPINGSTRATEGIES22')
IMG_CONSUMPTION22  =  config('IMG_CONSUMPTION22')
IMG_TOTALV222  =  config('IMG_TOTALV222')

# 2023
IMG_EDUCATION23  =  config('IMG_EDUCATION23')
IMG_FOOD23  =  config('IMG_FOOD23')
IMG_HEALTH23  =  config('IMG_HEALTH23')
IMG_WATER23  =  config('IMG_WATER23')
IMG_SANITATION23  =  config('IMG_SANITATION23')
IMG_HANDWASHING23  =  config('IMG_HANDWASHING23')
IMG_OVERCROWDING23  =  config('IMG_OVERCROWDING23')
IMG_HOUSING23  =  config('IMG_HOUSING23')
IMG_FUEL23  =  config('IMG_FUEL23')
IMG_ELECTRICITY23  =  config('IMG_ELECTRICITY23')
IMG_ASSETS23  =  config('IMG_ASSETS23')
IMG_LIVELIHOODBASEDCOPINGSTRATEGIES23 =  config('IMG_LIVELIHOODBASEDCOPINGSTRATEGIES23')
IMG_CONSUMPTION23  =  config('IMG_CONSUMPTION23')
IMG_TOTALV223  =  config('IMG_TOTALV223')
