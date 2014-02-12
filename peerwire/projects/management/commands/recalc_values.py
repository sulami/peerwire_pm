from django.core.management.base import BaseCommand, CommandError
from projects.models import Project

class Command(BaseCommand):
    help = 'Recalculates values for projects, decrements them at midnight'

    def handle(self, *args, **options):
        for p in Project.objects.all():
            # Active projects
            if p.status == 1:
                p.value *= .9
                p.save()
            # Inactive projects
            else:
                p.value = 0
                p.save()

