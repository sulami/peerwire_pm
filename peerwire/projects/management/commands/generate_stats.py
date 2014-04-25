from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from projects.models import *

class Command(BaseCommand):
    help = 'Generates static HTML with Peerwire\'s statistics'

    def handle(self, *args, **options):
        p_all = 0
        p_active = 0
        p_inactive = 0
        p_root = 0
        p_langs = {}
        for l in Lang.objects.all():
            p_langs[l] = 0
        for p in Project.objects.all():
            if p.status == 'Active':
                p_active += 1
            else:
                p_inactive += 1
            if not p.parent:
                p_root += 1
            for l in p.langs.all():
                p_langs[l] += 1
            p_all += 1
        u_all = 0
        for u in User.objects.all():
            u_all += 1
        langs = {}
        for l in UserLang.objects.all():
            langs[l.lang] = 0
        for l in UserLang.objects.all():
            langs[l.lang] += 1

        print("\nGeneral Statistics:")
        print("       Projects: %d (%d active, %d inactive, %d root)" %
            (p_all, p_active, p_inactive, p_root))
        print("          Users: %d" % u_all)
        print("\nUser Languages:")
        for l, i in langs.iteritems():
            print("%s: %d" % (str(l).rjust(15), i))
        print("\nProject Languages:")
        for l, i in p_langs.iteritems():
            if i != 0:
                print("%s: %d" % (str(l).rjust(15), i))

