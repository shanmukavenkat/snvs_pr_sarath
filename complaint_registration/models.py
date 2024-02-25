from django.db import models
from user_administration.models import CustomUser
import uuid
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _


# Our user model
class Complaint(models.Model):
    complaint_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=False)
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_time = models.TimeField(auto_now_add=True)
    complaint_message = models.CharField(max_length=1000, editable=True)
    type_of_complaint = models.CharField(editable=True, default='public')
    status = models.CharField(editable=True, default='pending')
    complaint_title = models.CharField(max_length=100, editable=True)
    groups = models.ManyToManyField(
        Group,
        help_text=_('The group this complaint belongs to'),
        verbose_name=_('groups'),
        related_name=_('complaints')
    )

    def __str__(self):
        return f'Complaint by {self.user.username} at {self.complaint_time}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.type_of_complaint == 'public':
            public = Group.objects.get(name='public')
            self.groups.add(public)

        elif self.type_of_complaint == 'sensitive':
            sensitive = Group.objects.get(name='sensitive')
            self.groups.add(sensitive)