from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# /
def blank(request):
    return redirect("/home")

def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


# /login
def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def register(request):
    template = loader.get_template('register.html')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = UserCreationForm()

    context = {"form": form}
    return HttpResponse(template.render(context, request))
