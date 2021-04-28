from django.contrib import admin
from .models import Enrolled_Class
from django.contrib import admin


# Register your models here.
@admin.register(Enrolled_Class)
class Enrolled_ClassAdmin(admin.ModelAdmin):
    list_display = ['courseName', 'courseNumber', 'professor', 'startDate', 'meetingTime']

