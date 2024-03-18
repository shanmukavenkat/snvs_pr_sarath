from django.contrib import admin
from complaint_administration.models.complaint_models import Complaint
# Register your models here.


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_title', 'complaint_date', 'complaint_message', 'complaint_time', 'type_of_complaint',
                    'status', 'username', 'assigned_to', 'escalated_to')

    def username(self, obj):
        return obj.user_object.user.username