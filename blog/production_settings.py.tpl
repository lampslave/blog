import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = ''

ALLOWED_HOSTS = ['lampslave.ru', 'www.lampslave.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'blog',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST': {
            'NAME': 'blog_test',
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, '../blog-static')
