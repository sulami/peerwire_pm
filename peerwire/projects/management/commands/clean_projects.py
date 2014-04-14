from django.core.management.base import BaseCommand, CommandError
from projects.models import Project

class Command(BaseCommand):
    help = 'Deletes projects without owners'

    def handle(self, *args, **options):
        count = 0
        for p in Project.objects.all():
            if p.owners.all().count() == 0:
                print "Deleting:", p
                count += 1
                p.delete()
        print "Deleted %d projects." % count
