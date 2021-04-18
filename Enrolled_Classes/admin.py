from django.contrib import admin
from .models import Enrolled_Class, Meeting_Day


# Register your models here.
@admin.register(Enrolled_Class)
class Enrolled_ClassAdmin(admin.ModelAdmin):
    list_display = ['courseName', 'courseNumber', 'professor', 'startDate', 'meetingTime']

@admin.register(Meeting_Day)
class Meeting_DayAdmin(admin.ModelAdmin):
    list_display = ['course', 'meetingDate', 'meetingTime']

