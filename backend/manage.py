#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pytest
import subprocess

def run_tests():
    print("Running tests before server startup...")

    env = os.environ.copy()
    env["TESTING"] = "true"  

    result = subprocess.run(
        ["pytest", "-v", "--tb=short"],
        env=env
    )

    if result.returncode != 0:
        print("Some tests failed! Server will not start.")
        sys.exit(1)

    print("All tests passed! Starting the server...")
    
def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
    
    if "runserver" in sys.argv:
        run_tests()
    
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
