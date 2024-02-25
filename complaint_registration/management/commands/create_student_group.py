from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        student = Group.objects.create(name='student')

        modify_complaint_permission = Permission.objects.get(codename='modify_complaint')
        create_complaint_permission = Permission.objects.get(codename='create_complaint')

        student.permissions.add(modify_complaint_permission)
        student.permissions.add(create_complaint_permission)
