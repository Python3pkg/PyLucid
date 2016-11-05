#!/usr/bin/env python3
# coding: utf-8

"""
    PyLucid
    ~~~~~~~

    run all tests:

    (PyLucid_env) ~/PyLucid_env/src/pylucid $ ./runtests.py

    run only some tests, e.g.:

    (PyLucid_env) ~/PyLucid_env/src/pylucid $ ./runtests.py tests.test_file
    (PyLucid_env) ~/PyLucid_env/src/pylucid $ ./runtests.py tests.test_file.test_class
    (PyLucid_env) ~/PyLucid_env/src/pylucid $ ./runtests.py tests.test_file.test_class.test_method

    :copyleft: 2015-2016 by the PyLucid team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import sys

import pytest

if sys.version_info < (3, 4):
    print("\nERROR: PyLucid requires Python 3.4 or greater!\n")
    sys.exit(101)

import django

from pylucid_installer.page_instance_template import example_project

# Made the 'example_project' importable to use it in unittests
sys.path.append(
    os.path.join(os.path.dirname(example_project.__file__), os.pardir)
)


def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()

    sys.exit(pytest.main())


if __name__ == "__main__":
    run_tests()

