# -*- coding: utf-8 -*-
"""
Django related management commands.

Those commands replace the usage of ``./manage.py`` (thus it's removed). Those
correspond 1 to 1 to their ``./manage.py`` counterparts but the arguments are
in the fabric format (can't get around this).
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import sys
from os import environ

# local imports
from . import config as conf


def _manage_cmd(cmd, settings=None):
    """ Run django ./manage.py command manually.

    This function eliminates the need for having ``manage.py`` (reduces file
    clutter).
    """
    sys.path.insert(0, conf.SRC_DIR)

    settings = settings or conf.get('DJANGO_SETTINGS', None)
    environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    args = sys.argv[0:-1] + cmd

    execute_from_command_line(args)


def devserver(settings=None, port=8000):
    """ Run dev server. """
    _manage_cmd(['runserver', '0.0.0.0:{}'.format(port)], settings)


def collectstatic():
    """ Collect all static files. """
    _manage_cmd(['collectstatic', '--no-input'])


def mkmigrations(app, name):
    """ Create migrations for a given app. """
    _manage_cmd(['makemigrations', '-n', name] + app.split(' '))


def migrate():
    """ Apply pending migrations. """
    _manage_cmd(['migrate'])


def createsuperuser():
    """ Create super user (probably needed for the first user). """
    _manage_cmd(['createsuperuser'])


def shell():
    """ Start django shell """
    _manage_cmd(['shell'])
