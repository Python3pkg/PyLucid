# coding: utf-8

"""
    PyLucid unittest base class
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author: JensDiemer $

    :copyleft: 2009 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from django.test import TransactionTestCase
from django.contrib.sites.models import Site

from django_tools.unittest.unittest_base import BaseTestCase

class BaseUnittest(BaseTestCase, TransactionTestCase):
    def login(self, usertype):
        """
        Login test user.
        Add him to the site, otherwise he can't login ;)
        """
        site = Site.objects.get_current()
        user = self._get_user(usertype="normal")

        from pylucid.models import UserProfile
        try:
            userprofile = user.get_profile()
        except UserProfile.DoesNotExist:
            # FIXME: Why does in some case user.get_profile() not work???
            userprofile = UserProfile.objects.get(user=user)

        if not site in userprofile.site.all():
            print "Info: Add user to site %s" % site
            userprofile.site.add(site)

        ok = self.client.login(username=self.TEST_USERS[usertype]["username"],
                               password=self.TEST_USERS[usertype]["password"])
        self.failUnless(ok, "Can't login test user '%s'!" % usertype)
        return user

