from django.contrib import admin
from Attendance.models import Meeting_Day


@admin.register(Meeting_Day)
class Meeting_DayAdmin(admin.ModelAdmin):
    list_display = ['course', 'meetingDate', 'meetingTime']