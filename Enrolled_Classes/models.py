from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Enrolled_Class(models.Model):
    courseName = models.CharField(max_length=120)  # Operating System Concepts
    courseNumber = models.CharField(max_length=8)  # CS4348
    sectionNumber = models.CharField(max_length=4)  # 004
    Course_Description = models.TextField(max_length=500, blank=True)
    startDate = models.DateTimeField(blank=True, null=True)
    meetingTime = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField(User, blank=True, related_name="students")
    def __str__(self):
        return self.courseName


class Meeting_Day(models.Model):
    meetingDate = models.DateTimeField(blank=True, null=True)
    meetingTime = models.DateTimeField(blank=True, null=True)
    course = models.ForeignKey(Enrolled_Class, on_delete=models.CASCADE, blank=True, null=True, related_name="course")
    present = models.ManyToManyField(User, blank=True, related_name="present")
    late = models.ManyToManyField(User, blank=True, related_name="late")
    absent = models.ManyToManyField(User, blank=True, related_name="absent")
    not_applicable = models.ManyToManyField(User, blank=True, related_name="not_applicable")

    def __str__(self):
        return self.course