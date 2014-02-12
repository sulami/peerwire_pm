from django.core.management.base import BaseCommand, CommandError
from projects.models import Project

class Command(BaseCommand):
    help = 'Recalculates values for projects, decrements them at midnight'

    def handle(self, *args, **options):
        # Active projects
        for p in Project.objects.filter(status=1):
            p.value *= .9
            p.save()
        # Inactive projects
        for p in Project.objects.filter(status=0):
            p.value = 0
            p.save()

