# coding: utf-8

"""
    Create pages for djangocms-blog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2015 by the PyLucid team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import unicode_literals

import sys
import logging
from optparse import make_option
import datetime
import time
import atexit

from django.db import transaction
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.utils.translation import activate
from django.conf import settings
from django.core.management.base import BaseCommand

from pylucid_migration.models import DjangoSite

MIGRATE_ALL_SITES = "ALL"


def site_option(option, opt, value, parser):
    """
    optparse callback for: --sites
    """
    if not value:
        value = settings.SITE_ID
    else:
        value = value.strip()
        if value.upper() == MIGRATE_ALL_SITES.upper():
            value = MIGRATE_ALL_SITES
        else:
            value = [int(id) for id in value.split(',')]

    setattr(parser.values, option.dest, value)



class StatusLine(object):
    """
    Simple helper to display process information.
    Will only work under Linux!
    """
    def __init__(self, total_count=None):
        self.total_count=total_count

    def __enter__(self):
        self.start_time = time.time()
        return self

    def write(self, no, txt):
        elapsed = time.time() - self.start_time
        estimated = elapsed / no * self.total_count
        remain = estimated-elapsed

        if remain>60:
            time_info = "%.1fmin" % (remain/60)
        else:
            time_info = "%.1fsec" % remain

        txt = "[%i/%i %s] %s" % (no, self.total_count, time_info, txt)
        print('\r\x1b[K%s' % txt, end='', flush=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print()
        duration = time.time() - self.start_time
        print("process duration: %.2fsec." % duration)


class TeeOutput(object):
    """
    redirect output to logfile and origin stdout
    e.g.:
        sys.stderr = TeeOutput(sys.stderr, self.my_logger.error)
    """
    def __init__(self, origin, file_log_func):
        self.origin = origin
        self.file_log_func = file_log_func

    def write(self, txt):
        for line in txt.rstrip().splitlines():
            self.file_log_func(line)
        self.origin.write(txt)


class MigrateBaseCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--inline_script',
            action='store_true',
            dest='inline_script',
            default=False,
            help='Move inline javascript into "html" markup entry.'
        ),
        make_option('--sites', dest="sites", type='string', action='callback',
            callback=site_option, default=None,
            help=(
                "Which SITE_ID should be migrated?"
                " If not set: Only the current settings.SITE_ID will be migrated."
                " Use a comma separated list of SITE_IDs."
                " Use '%s' for all existing sites."
            ) % MIGRATE_ALL_SITES
        ),
        make_option('--site_info',
            action='store_true',
            dest='site_info',
            default=False,
            help='Print a list of all existing sites and quit.'
        ),
    )

    def _site_info(self):
        self.stdout.write("\nList of old SITE_ID entries:")
        for site in DjangoSite.objects.all():
            self.stdout.write("\tID: %i - name: %r - domain: %r" % (site.pk, site.name, site.domain))

    def _migrate_sites(self, options):
        sites = []

        self.stdout.write("\nMigrate Sites (%s):" % repr(options["sites"]))
        
        if not options["sites"]:
            old_sites = DjangoSite.objects.all().filter(pk=settings.SITE_ID)
        elif options["sites"] == MIGRATE_ALL_SITES:
            old_sites = DjangoSite.objects.all()
        else:
            old_sites = DjangoSite.objects.all().filter(pk__in=options["sites"])

        for site_old in old_sites:
            try:
                site_new = Site.objects.get(pk=site_old.pk)
            except Site.DoesNotExist:
                site_new = Site.objects.create(
                    pk=site_old.pk,
                    domain=site_old.domain,
                    name=site_old.name,
                )
                self.stdout.write("\tNew site %r with ID %i created." % (site_new.name, site_new.id))
            else:
                self.stdout.write("\tSite %r with ID %i exists, ok." % (site_new.name, site_new.id))

            sites.append(site_new)

        return sites


    def handle(self, *args, **options):
        if options["site_info"]:
            self._site_info()
            sys.exit()

        self.file_log=logging.getLogger(name="PyLucidMigration")

        # self.logfilename="%s-PyLucidMigration.log" % datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        self.logfilename="%s-PyLucidMigration.log" % datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M")
        # self.logfilename="%s-PyLucidMigration.log" % datetime.datetime.utcnow().strftime("%Y%m%d")
        handler = logging.FileHandler(self.logfilename, mode='w', encoding="utf8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.file_log.addHandler(handler)
        print("\nLog into %r" % self.logfilename)

        self.file_log.debug("_"*79)
        self.file_log.debug("Start logging for: %r" % " ".join(sys.argv))

        atexit.register(self.goodbye)

        sys.stderr = TeeOutput(sys.stderr, self.file_log.error)

        self.sites = self._migrate_sites(options)

    def goodbye(self):
        print("\nPlease look into log file: %r" % self.logfilename)
