from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def enrolledClasses_view(request):
    template = loader.get_template('enrolled_classes/enrolledClasses.html')
    context = {}

    return HttpResponse(template.render(context, request))

def addClass_view(request):
    template = loader.get_template('enrolled_classes/addClass.html')
    context = {}

    return HttpResponse(template.render(context, request))