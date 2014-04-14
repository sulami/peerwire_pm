from django.core.management.base import BaseCommand, CommandError
from projects.models import Project
import datetime

class Command(BaseCommand):
    help = 'Deletes projects queued for deletion/without owners'

    def handle(self, *args, **options):
        count = 0
        for p in Project.objects.all():
            if p.owners.all().count() == 0 or p.del_t == datetime.date.today():
                print "Deleting:", p
                count += 1
                p.delete()
        print "Deleted %d projects." % count
