from django.db import models
from Register.models import Profile


# Create your models here.
class Enrolled_Class(models.Model):
    courseName = models.CharField(max_length=120)  # Operating System Concepts
    courseNumber = models.CharField(max_length=8)  # CS4348
    sectionNumber = models.CharField(max_length=4)  # 004
    Course_Description = models.TextField(max_length=500)
    studentList = models.ManyToManyField(Profile)

    def __str__(self):
        return self.courseName