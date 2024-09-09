import ee, os

DATA_DIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+vr@tllmv-*s*5jl#5ha^x+_2#zyp+!+m$(c^jd5-nu#cb2%+9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

GOOGLE_ANALYTICS_ID = 'G-Z5J9SXL16P'

GOOGLE_OAUTH2_CLIENT_ID = ''

GOOGLE_MAPS_API_KEY = ''


# GEE authentication
# The service account email address authorized by your Google contact.

EE_ACCOUNT = 'khpovertymapping@servir-ee.iam.gserviceaccount.com'
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


MAPBOX_API_KEY = 'pk.eyJ1Ijoic2VydmlybWVrb25nIiwiYSI6ImNrYWMzenhldDFvNG4yeXBtam1xMTVseGoifQ.Wr-FBcvcircZ0qyItQTq9g'

EE_TASK_POLL_FREQUENCY = 10
# GEE collection
NIGHTLIGHT = "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG"
TREE_CANOPY ="projects/servir-mekong/UMD/tree_canopy"
TREE_HEIGHT ="projects/servir-mekong/UMD/tree_height"
LANDCOVER = "projects/cemis-camp/assets/landcover/lcv3/"
VALNERABILITY_AMD3 = "projects/cambodiapovertymapping/assets/undp/adm3_50v2/all_50"

ADM3 = "projects/cambodiapovertymapping/assets/undp/website/basemap/adm3"
ADM2 = "projects/cambodiapovertymapping/assets/undp/website/basemap/adm2"
ADM1 = "projects/cambodiapovertymapping/assets/undp/website/basemap/adm1"
ADM0 = "projects/earthengine-legacy/assets/projects/servir-mekong/admin/KHM_adm0"

POP_ADM1 = "projects/cambodiapovertymapping/assets/undp/website/populationAdm1"
POP_ADM2 = "projects/cambodiapovertymapping/assets/undp/website/populationAdm2"
POP_ADM3 = "projects/cambodiapovertymapping/assets/undp/website/populationAdm3"
DEPRIVATIONIMG = "projects/cambodiapovertymapping/assets/undp/website/deprivationsImg100"
BUILDINGS_POP = "projects/cambodiapovertymapping/assets/undp/buildingsWithPeople/buildingsWithPeopleImg"

IMG_BUILDINGS  = "projects/servir-mekong/buildings/cambodiaFinal"
IMG_EDUCATION  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/EducationalAttainmentv2"
IMG_SCHOOL  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/SchoolAttendancev2"
IMG_FOOD  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/FoodConsumptionScorev2"
IMG_HEALTH  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstohealthcarev2"
IMG_WATER  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstocleanwaterv2"
IMG_SANITATION  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/AccesstoSanitationv2"
IMG_HANDWASHING  = "projects/servir-mekong/undp/indicators/HandWashingv2"
IMG_OVERCROWDING  = "projects/servir-mekong/undp/indicators/overcrowdingv2"
IMG_HOUSING  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Housingmaterialsv2"
IMG_FUEL  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Cookingfuelv2"
IMG_ELECTRICITY  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/accesstoelectricityv2"
IMG_ASSETS  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Assetsv2"
IMG_LIVELIHOODBASEDCOPINGSTRATEGIES = "projects/servir-mekong/undp/indicators/LivelihoodBasedCopingStrategiesv2"
IMG_CONSUMPTION  = "projects/servir-mekong/undp/indicators/ConsumptionandExpenditurev2"
IMG_TOTALV2  = "projects/servir-mekong/undp/indicators/totalv2"

HEALTH_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstohealthcare"
ASSETS_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Assets"
FUEL_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Cookingfuel"
EDUCATION_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/EducationalAttainment"
FOOD_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/FoodConsumptionScore"
HOUSING_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Housingmaterials"
SCHOOL_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/SchoolAttendance"
ELECTRICITY_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/accesstoelectricity"
CONSUMPTION_IMG = "projects/servir-mekong/undp/indicators/ConsumptionandExpenditure"
BUILDING_FC = "projects/servir-mekong/buildings/cambodia"
SANITATION_IMG = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/AccesstoSanitation"
WATER_IMG  = "projects/earthengine-legacy/assets/projects/servir-mekong/undp/indicators/Accesstocleanwater"
