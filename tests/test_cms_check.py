# coding: utf-8

"""
    PyLucid
    ~~~~~~~

    :copyleft: 2016 by the PyLucid team, see AUTHORS for more details.
    :created: 2016 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import pytest

from .test_utils.test_cases import PageInstanceTestCase


@pytest.mark.django_db
class CmsCheckTest(PageInstanceTestCase):

    def test_django_check(self):
        """ ./manage.py check """
        output = self.call_manage_py(["check"])
        # print(output)
        self.assertNotIn("ERROR", output)
        self.assertIn("System check identified no issues (0 silenced).", output)

    def test_cms_check(self):
        self.call_manage_py(["migrate", "--noinput"])
        output = self.call_manage_py(["cms", "check"])

        self.assertNotIn("ERROR", output)
