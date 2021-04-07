from django.http import HttpResponse
from django.template import loader


# /
def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


# /login
def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))
