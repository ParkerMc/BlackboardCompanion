from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Enrolled_Class
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_view(request):
    template = loader.get_template('enrolled_classes/enrolledClasses.html')
    context = {}

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def addClass_view(request):
    template = loader.get_template('enrolled_classes/addClass.html')
    context = {}
    if request.method == "POST":
        courseName = request.POST["CourseName"]
        sectionNum = request.POST["Section"]
        courseCode = request.POST["Course"]



        return redirect("/home")

    return HttpResponse(template.render(context, request))