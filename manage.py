#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# Fix for Russian Windows locale: libpq returns error messages in CP1251,
# which psycopg2 fails to decode as UTF-8. Setting PGCLIENTENCODING forces UTF8.
os.environ.setdefault("PGCLIENTENCODING", "UTF8")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "team_finder.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
