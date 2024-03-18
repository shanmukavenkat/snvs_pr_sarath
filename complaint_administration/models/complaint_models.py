from django.db import models
from user_administration.escalation_models import EscalationStructure
import uuid
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Our user model
class Complaint(models.Model):
    complaint_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='complaint_user')
    user_id = models.PositiveIntegerField()
    user_object = GenericForeignKey('user_type', 'user_id')
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_time = models.TimeField(auto_now_add=True)
    complaint_message = models.CharField(max_length=1000, editable=True)
    type_of_complaint = models.CharField(editable=True, default='public')
    status = models.CharField(editable=True, default='pending')
    complaint_title = models.CharField(max_length=100, editable=True)

    # Should be able to assign to multiple models such as Counsellor, ClassTeacher, HOD
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE, related_name='complaint_owner')
    object_id = models.PositiveIntegerField()
    assigned_to = GenericForeignKey('content_type', 'object_id')

    escalated_to = models.ForeignKey(to=EscalationStructure, on_delete=models.CASCADE)

    groups = models.ManyToManyField(
        Group,
        help_text=_('The group this complaint belongs to'),
        verbose_name=_('groups'),
        related_name=_('complaints')
    )

    def __str__(self):
        return f'Complaint by {self.user_object.user.username} at {self.complaint_time}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.type_of_complaint == 'public':
            public = Group.objects.get(name='public')
            self.groups.add(public)

        elif self.type_of_complaint == 'sensitive':
            sensitive = Group.objects.get(name='sensitive')
            self.groups.add(sensitive)