#!/usr/bin/env python
import django
import sys
from django.core.management import execute_from_command_line
from django.conf import settings


def setup():
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


if __name__ == '__main__':
    setup()
    argv = sys.argv[:]
    argv.insert(1, 'test')
    execute_from_command_line(argv)
