import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(os.path.join(__file__, '../')))
)

SHARED_URL = "https://shared.acdh.oeaw.ac.at/"
PROJECT_NAME = "djangobaseproject"


ACDH_IMPRINT_URL = "https://shared.acdh.oeaw.ac.at/acdh-common-assets/api/imprint.php?serviceID="
REDMINE_ID = 10459

# Application definition

INSTALLED_APPS = [
    'dal',
    'django.contrib.admin',
    'dal_select2',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'crispy_forms',
    'django_filters',
    'django_tables2',
    'rest_framework',
    'webpage',
    'browsing',
    'vocabs',
    'infos',
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'djangobaseproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webpage.webpage_content_processors.installed_apps',
                'webpage.webpage_content_processors.is_dev_version',
                'webpage.webpage_content_processors.get_db_name',
                "webpage.webpage_content_processors.shared_url",
                "webpage.webpage_content_processors.my_app_name",
            ],
        },
    },
]

WSGI_APPLICATION = 'djangobaseproject.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

ARCHE_SETTINGS = {
    'project_name': ROOT_URLCONF.split('.')[0],
    'base_url': "https://id.acdh.oeaw.ac.at/{}".format(ROOT_URLCONF.split('.')[0])
}

VOCABS_DEFAULT_PEFIX = "changeme"

VOCABS_SETTINGS = {
    'default_prefix': VOCABS_DEFAULT_PEFIX,
    'default_nsgg': f"http://www.vocabs/{VOCABS_DEFAULT_PEFIX}/",
    'default_lang': "en"
}
