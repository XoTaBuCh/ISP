import os

DOCKER = True

if DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': 5432,
            'TEST': {
                'NAME': 'tester',
            },
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lab3',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': 5432,
            'TEST': {
                'NAME': 'tester',
            },
        }
    }