from django.contrib.auth.models import User
from django.db import models
from Enrolled_Classes.models import Enrolled_Class


class Meeting_Day(models.Model):
    meetingDate = models.CharField(max_length=14, blank=True, null=True)
    meetingTime = models.TimeField(blank=True, null=True)
    course = models.ForeignKey(Enrolled_Class, on_delete=models.CASCADE, blank=True, null=True, related_name="course")
    present = models.ManyToManyField(User, blank=True, related_name="present")
    late = models.ManyToManyField(User, blank=True, related_name="late")
    absent = models.ManyToManyField(User, blank=True, related_name="absent")
    not_applicable = models.ManyToManyField(User, blank=True, related_name="not_applicable")
    randomString = models.CharField(max_length=11, blank=False, null=False)

    def __str__(self):
        return self.course.courseName