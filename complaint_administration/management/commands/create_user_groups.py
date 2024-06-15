from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


def create_group_with_permissions(group_name: str, permissions: list[str]):
    group_object = Group.objects.get_or_create(name=group_name)
    group_object = group_object[0]
    for permission in permissions:
        retrieved_permission = Permission.objects.get(codename=permission)
        group_object.permissions.add(retrieved_permission)


class Command(BaseCommand):
    def handle(self, *args, **options):
        permissions = [
            'create_complaint',
            'modify_complaint',
            'view_sensitive_complaint',
            'dismiss_complaint',
            'escalate_complaint',
            'assign_complaint',
        ]

        groups_with_permissions = [
            ('Student', ('create_complaint', 'modify_complaint')),
            ('Counsellor', ('create_complaint', 'modify_complaint', 'escalate_complaint')),
            ('ClassTeacher', ('create_complaint', 'modify_complaint', 'escalate_complaint', 'assign_complaint')),
            ('HeadOfDepartment', ('create_complaint', 'modify_complaint', 'escalate_complaint', 'dismiss_complaint',
                                  'assign_complaint'))
        ]

        # Creating all the groups
        for item in groups_with_permissions:
            (group_name, (permissions)) = item
            create_group_with_permissions(group_name, permissions)
