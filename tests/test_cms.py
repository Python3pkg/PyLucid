# coding: utf-8

"""
    PyLucid
    ~~~~~~~

    :copyleft: 2016 by the PyLucid team, see AUTHORS for more details.
    :created: 2016 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import pytest

from cms.api import create_page, create_title, add_plugin
from cms.constants import TEMPLATE_INHERITANCE_MAGIC

from django_tools.unittest_utils.BrowserDebug import debug_response
from django_tools.unittest_utils.unittest_base import BaseTestCase

from cms.test_utils.testcases import CMSTestCase
from tests.test_utils.test_cases import ExampleProjectMixIn


@pytest.mark.django_db
class CmsTests(ExampleProjectMixIn, CMSTestCase):
    def test_language_redirect_en(self):
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='en')
        # debug_response(response)
        self.assertRedirects(response,
            expected_url='http://testserver/en/',
            fetch_redirect_response = False # no page exist!
        )


@pytest.mark.django_db
class ExistingCmsPageTests(ExampleProjectMixIn, CMSTestCase, BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(ExistingCmsPageTests, cls).setUpClass()
        cls.page = create_page(
            title='english index',
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="en",
            published=True,
            in_navigation=True
        )
        create_title("de", "Deutsch Index", cls.page)
        cls.placeholder = cls.page.placeholders.get(slot='content')
        cls.text_plugin_en = add_plugin(
            placeholder=cls.placeholder,
            plugin_type="TextPlugin", # djangocms_text_ckeditor
            language="en",
            body="Hello World!"
        )
        cls.page.publish("en")
        cls.text_plugin_de = add_plugin(
            placeholder=cls.placeholder,
            plugin_type="TextPlugin", # djangocms_text_ckeditor
            language="de",
            body="Hallo Welt!"
        )
        cls.page.publish("de")

    def test_language_redirect_en(self):
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='en')
        # debug_response(response)
        self.assertRedirects(response,
            expected_url='http://testserver/en/',
        )

    def test_language_redirect_de(self):
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='de')
        # debug_response(response)
        self.assertRedirects(response,
            expected_url='http://testserver/de/',
        )

    def test_url_en(self):
        url = self.page.get_absolute_url(language="en")
        self.assertEqual(url, "/en/")

    def test_url_de(self):
        url = self.page.get_absolute_url(language="de")
        self.assertEqual(url, "/de/")

    def test_request_en(self):
        response = self.client.get('/en/', HTTP_ACCEPT_LANGUAGE='en')
        # debug_response(response)
        self.assertResponse(response,
            must_contain=("Hello World!",),
            must_not_contain=("error", "Traceback"),
            status_code=200, html=False,
            browser_traceback=True
        )

    def test_request_de(self):
        response = self.client.get('/de/', HTTP_ACCEPT_LANGUAGE='de')
        # debug_response(response)
        self.assertResponse(response,
            must_contain=("Hallo Welt!",),
            must_not_contain=("error", "Traceback"),
            status_code=200, html=False,
            browser_traceback=True
        )



