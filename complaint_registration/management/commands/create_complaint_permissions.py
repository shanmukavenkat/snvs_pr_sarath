from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from complaint_registration.models import Complaint
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Complaint)

        Permission.objects.create(
            name='Can create a complaint',
            codename='create_complaint',
            content_type=content_type,
        )

        Permission.objects.create(
            name='Can modify complaint',
            codename='modify_complaint',
            content_type=content_type
        )
