from django.contrib import admin
from .models import Complaint
# Register your models here.


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_title', 'complaint_date', 'complaint_message', 'complaint_time', 'type_of_complaint', 'status',
                    'user_username')

    def user_username(self, obj):
        return obj.user.username