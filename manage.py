#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opendatapdx.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    # Install fixtures (this should probably be done using migrations)
    #if len(sys.argv) == 2 and sys.argv[1] == 'migrate':
    #    execute_from_command_line(['manage.py', 'loaddata', 'initial_data.json'])

