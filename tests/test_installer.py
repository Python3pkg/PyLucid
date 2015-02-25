# coding: utf-8

"""
    PyLucid
    ~~~~~~~

    :copyleft: 2015 by the PyLucid team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
from unittest import TestCase
import sys

from click.testing import CliRunner

from pylucid_installer.pylucid_installer import cli
from tests.test_utils.test_cases import PageInstanceTestCase



class PyLucidInstallerCLITest(TestCase):
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli [OPTIONS]", result.output)
        # print(result.output)

    def test_dest_exists(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as temp_path:
            result = runner.invoke(cli, [
                "--dest", temp_path,
                "--name", "test_remove_question",
            ])
            # print(result.output)
            self.assertIn("ERROR: Destination '%s' exist!" % temp_path, result.output)
            self.assertEqual(result.exit_code, 2)
            self.assertEqual(os.listdir(temp_path), [])

    def test_remove_question(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as temp_path:
            result = runner.invoke(cli, [
                "--dest", temp_path,
                "--name", "test_remove_question",
                "--remove"
            ])
            # print(result.output)
            self.assertIn(
                "Delete '%s' before copy? [y/N]:" % temp_path,
                result.output
            )
            self.assertEqual(result.exit_code, 1)
            self.assertEqual(os.listdir(temp_path), [])

    def test_unuseable_name(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as temp_path:
            result = runner.invoke(cli, [
                "--dest", temp_path,
                "--name", "a unuseable name!",
            ],
            )
            # print(result.output)

            self.assertIn(
                "ERROR: The given project name is not useable!",
                result.output
            )
            self.assertIn(
                "a_unuseable_name",
                result.output
            )
            self.assertEqual(result.exit_code, 1)

    def test_create(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as temp_path:
            result = runner.invoke(cli, [
                "--dest", temp_path,
                "--name", "unittest_project",
                "--remove"
            ],
                input="y"
            )
            # print(result.output)
            self.assertIn(
                "Delete '%s' before copy? [y/N]:" % temp_path,
                result.output
            )
            self.assertEqual(result.exit_code, 0)

            self.assertIn(
                "Page instance created here: '%s'" % temp_path,
                result.output
            )
            self.assertListEqual(
                os.listdir(temp_path),
                ['static', 'manage.py', 'unittest_project']
            )

            # Check patched manage.py
            with open(os.path.join(temp_path, "manage.py"), "r") as f:
                shebang = f.readlines(1)
                self.assertEqual(shebang, ["#!%s\n" % sys.executable])

                content = f.read()
                # print(content)
                self.assertIn(
                    'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unittest_project.settings")',
                    content
                )

            # Check patched settings.py
            with open(os.path.join(temp_path, "unittest_project", "settings.py"), "r") as f:
                content = f.read()
                # print(content)
                self.assertIn(
                    'DOC_ROOT = "%s"' % temp_path,
                    content
                )
                self.assertIn(
                    "ROOT_URLCONF = 'unittest_project.urls'",
                    content
                )


class ManageTest(PageInstanceTestCase):
    # def test_debug_settings(self):
    #     with open(os.path.join(self.project_path, "settings.py"), "r") as f:
    #         content = f.read()
    #         print(content)

    def test_help(self):
        status, output = self.call_manage_py(["--help"])
        # print(output)

        self.assertIn("Usage: manage.py subcommand [options] [args]", output)
        self.assertIn("[pylucid]", output)
        self.assertIn("create_blog_page", output)
        self.assertEqual(status, 0)

    def test_check(self):
        status, output = self.call_manage_py(
            ["check"],
            # debug=True
        )
        self.assertNotIn("ImproperlyConfigured", output)
        self.assertEqual(status, 0)

    def test_diffsettings(self):
        # self.dont_cleanup_temp=True

        status, output = self.call_manage_py(
            ["diffsettings"],
            # debug=True
        )
        self.assertNotIn("ImproperlyConfigured", output)
        self.assertIn(
            "PROJECT_DIR = '%s'" % self.project_path,
            output
        )
        self.assertIn(
            "STATIC_ROOT = '%s/static'" % self.temp_path,
            output
        )
        self.assertIn(
            "STATICFILES_DIRS = ('%s/static',)" % self.project_path,
            output
        )
        self.assertIn(
            "MEDIA_ROOT = '%s/media'" % self.temp_path,
            output
        )
        self.assertEqual(status, 0)

    def test_migrate(self):
        status, output = self.call_manage_py(
            ["migrate", "--noinput"],
            # debug=True
        )
        self.assertIn("Running migrations:", output)
        self.assertIn("Applying auth.", output)
        self.assertIn("Applying cms.", output)
        self.assertIn("Applying djangocms_blog.", output)
        self.assertEqual(status, 0)