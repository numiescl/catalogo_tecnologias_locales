from .local_settings import *


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'captcha',
    'cookielaw',
    'taggit',
    'catalogo'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tcc_catalogo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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
WSGI_APPLICATION = 'tcc_catalogo.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Catálogo de Tecnologías Locales",
    "site_header": "Catálogo",
    "site_brand": "Catálogo Tecnologías Locales",
    "site_logo": "img/favicon/favicon.svg",
    "site_logo_classes": "hidden",
    "welcome_sign": "Catálogo de Tecnologías Locales",
    "copyright": "Equipo Catálogo de Tecnologías Locales",
    "search_model": "catalogo.Tecnologia",
    "user_avatar": None,

    "topmenu_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Tecnologías", "model": "catalogo.Tecnologia", "permissions": ["auth.view_user"]},
        {"name": "Ilustraciones", "model": "catalogo:Tecnologia", "permissions": ["auth.view_user"]},
        {"name": "Drive", "url": "https://www.google.com", "new_window": True},
        {"name": "Ver el sitio", "url": "inicio"},
    ],

    "order_with_respect_to": ["auth", "catalogo.Tecnologia", "catalogo.Ilustracion", "catalogo.Realizador",
                              "catalogo.Localidad", "catalogo.Facilitador"],

    "icons": {
        "auth": "fas fa-id-card",
        "auth.user": "fas fa-user",
        "catalogo": "fas fa-folder-open",
        "catalogo.Tecnologia": "fas fa-file",
        "catalogo.Ilustracion": "fas fa-image",
        "catalogo.Realizador": "fas fa-user-cog",
        "catalogo.Localidad": "fas fa-globe-americas",
        "catalogo.Facilitador": "fas fa-user-tie",
    }

}
