#!/usr/bin/env python
import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        STATIC_URL='/static/',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django_nose',
            'django_google_maps.tests.test_app'
        ],
        MIDDLEWARE_CLASSES=[],
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
        NOSE_ARGS=[
            '--with-coverage',
            '--cover-package=django_google_maps',
        ]
    )

if hasattr(django, 'setup'):
    django.setup()


from django.core import management
management.call_command('test', 'django_google_maps.tests')
