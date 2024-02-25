from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        public = Group.objects.create(name='public')
        sensitive = Group.objects.create(name='sensitive')