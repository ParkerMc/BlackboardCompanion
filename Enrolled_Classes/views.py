from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def enrolledClasses_view(request):
    template = loader.get_template('enrolled_classes/enrolledClasses.html')
    context = {}

    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def addClass_view(request):
    template = loader.get_template('enrolled_classes/addClass.html')
    context = {}
    if request.method == "POST":
       coursename=request.POST["CourseName"]
       sectionnum=request.POST["Section"]
       codecourse=request.POST["Course"]
       print(coursename)
       return redirect("/enrolled-classes")

    return HttpResponse(template.render(context, request))