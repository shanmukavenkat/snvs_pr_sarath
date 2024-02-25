from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        counsellor = Group.objects.create(name='counsellor')

        modify_complaint_permission = Permission.objects.get(codename='modify_complaint')
        create_complaint_permission = Permission.objects.get(codename='create_complaint')

        counsellor.permissions.add(create_complaint_permission)
        counsellor.permissions.add(modify_complaint_permission)
        # Add other permissions
