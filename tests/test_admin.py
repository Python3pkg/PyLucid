# coding: utf-8

"""
    PyLucid
    ~~~~~~~

    :copyleft: 2016 by the PyLucid team, see AUTHORS for more details.
    :created: 2016 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import pytest

from django.test import Client

# https://github.com/jedie/django-tools
from django_tools.unittest_utils.BrowserDebug import debug_response
from django_tools.unittest_utils.unittest_base import BaseTestCase
from tests.test_utils.test_cases import ExampleProjectMixIn


@pytest.mark.django_db
class AdminAnonymousTests(ExampleProjectMixIn, BaseTestCase):
    def setUp(self):
        super(AdminAnonymousTests, self).setUp()
        self.client = Client()

    def test_lang_redirect_en(self):
        response = self.client.get('/admin/', HTTP_ACCEPT_LANGUAGE='en')
        # debug_response(response)
        self.assertRedirects(response,
            expected_url='http://testserver/en/admin/',
            fetch_redirect_response = False
        )

    def test_lang_redirect_de(self):
        response = self.client.get('/admin/', HTTP_ACCEPT_LANGUAGE='de')
        self.assertRedirects(response,
            expected_url='http://testserver/de/admin/',
            fetch_redirect_response = False
        )

    def test_login(self):
        """
        Anonymous will be redirected to the login page.
        """
        response = self.client.get('/en/admin/')
        # debug_response(response)
        self.assertRedirects(response, expected_url='http://testserver/en/admin/login/?next=/en/admin/')


@pytest.mark.django_db
class AdminLoggedinTests(AdminAnonymousTests):
    """
    Some basics test with the django admin
    """
    def setUp(self):
        super(AdminLoggedinTests, self).setUp()
        self.create_testusers()

    def test_staff_admin_index(self):
        self.login(usertype="staff")
        response = self.client.get('/en/admin/')
        self.assertResponse(response,
            must_contain=(
                "django CMS", "Django administration",
                "staff test user",
                "Site administration",
                "You don't have permission to edit anything."
            ),
            must_not_contain=("error", "traceback")
        )

    def test_supersuer_admin_index(self):
        self.login(usertype="superuser")
        response = self.client.get('/en/admin/')
        self.assertResponse(response,
            must_contain=(
                "django CMS", "Django administration",
                "superuser",
                "Site administration",

                "/admin/auth/group/add/",
                "/admin/auth/user/add/",

                "/admin/filer/folder/",
                "/admin/filer/thumbnailoption/add/",
            ),
            must_not_contain=("error", "traceback")
        )
