# coding: utf-8

"""
    PyLucid v1.x migration to django-cms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #!/bin/bash

    set -x
    rm example_project.db
    cp "fresh.db" example_project.db
    ./manage.py migrate pylucid_migration 0001_initial


    :copyleft: 2015 by the PyLucid team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import unicode_literals

from django.db import models, migrations




def forwards_func(apps, schema_editor):
    from cms.api import create_page, create_title
    import cms

    #PageTree = apps.get_model(u'pylucid_migration', "PageTree")
    from pylucid_migration.models import PageTree, PageMeta, PageContent

    tree = PageTree.objects.get_tree()

    pages = {}

    for node in tree.iter_flat_list():
        pagetree = PageTree.objects.get(id=node.id)
        url = pagetree.get_absolute_url()
        print(url)

        for pagemeta in PageMeta.objects.filter(pagetree=pagetree):
            url = pagemeta.get_absolute_url()
            print("\t%s" % url)

            if pagetree.parent:
                # print("parent: %r" % pagetree.parent.get_absolute_url())
                parent = pages[pagetree.parent.id]
            else:
                parent = None

            # http://docs.django-cms.org/en/support-3.0.x/reference/api_references.html#cms.api.create_page
            page = create_page(
                title=pagemeta.title,
                menu_title=pagemeta.name,

                template=cms.constants.TEMPLATE_INHERITANCE_MAGIC,
                language=pagemeta.language.code,
                slug=pagetree.slug,
                # apphook=None, apphook_namespace=None, redirect=None,
                meta_description=pagemeta.description,
                created_by='pylucid_migration',
                parent=parent,
                # publication_date=None, publication_end_date=None,
                # in_navigation=False, soft_root=False, reverse_id=None,
                # navigation_extenders=None, published=False,
                site=pagetree.site,
                # login_required=False, limit_visibility_in_menu=VISIBILITY_ALL,
                # position="last-child", overwrite_url=None, xframe_options=Page.X_FRAME_OPTIONS_INHERIT
            )
            pages[pagetree.id] = page



    # print("\n\n+++++++++++++++++++++++++++++++++++++++++\n\n")
    # raise NotImplementedError("Not ready, yet!")


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
