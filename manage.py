#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import dotenv
import os
import sys

from django.core.exceptions import ImproperlyConfigured


def check_environment():
    required_environment_variables = [ 'DATABASE_URL', 'SECRET_KEY' ]

    for name in required_environment_variables:
        if name not in os.environ:
            raise ImproperlyConfigured(f'The variable "{name}" is not set in your environment')


def main():
    dotenv.read_dotenv()
    check_environment()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectify_api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
