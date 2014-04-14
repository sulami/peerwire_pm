from django.core.management.base import BaseCommand, CommandError
from projects.models import User
import datetime

class Command(BaseCommand):
    help = 'Deletes users queued for deletion'

    def handle(self, *args, **options):
        count = 0
        for u in User.objects.all():
            if u.del_t == datetime.date.today():
                print "Deleting:", u
                count += 1
                p.delete()
        print "Deleted %d users." % count
