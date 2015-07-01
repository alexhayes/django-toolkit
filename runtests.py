#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django_nose',
            'django_toolkit',
            'django_toolkit.tests.testapp',
        ],
        # Django replaces this, but it still wants it. *shrugs*
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
        NOSE_ARGS=['--logging-clear-handlers',
                   # Coverage - turn on with NOSE_WITH_COVERAGE=1
                   '--cover-html',
                   '--cover-package=django_toolkit',
                   '--cover-erase',
                   '--with-fixture-bundling',
                   # Nose Progressive
                    '--with-progressive',
                   ]
    )


def runtests():
    test_args = sys.argv[1:] if len(sys.argv[1:]) > 0 else ['django_toolkit.tests']
    argv = sys.argv[:1] + ['test'] + test_args
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
