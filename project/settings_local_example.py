DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY='xCXO9UWitQ88szixBuuBTOUQkTYHV9pSbrLegCBWUzLd0lYpai'