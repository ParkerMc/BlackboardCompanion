from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# /
@login_required(login_url='/login/')
def blank_view(request):
    return redirect("/home")


@login_required(login_url='/login/')
def home_view(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


# /login
def login_view(request):
    template = loader.get_template('login.html')

    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        netID = request.POST['netid']
        password = request.POST['password']
        user = authenticate(request, username=netID, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.error(request, "The Username and/or Password are incorrect.")

    context = {}
    return HttpResponse(template.render(context, request))


def register_view(request):
    template = loader.get_template('register.html')

    if request.user.is_authenticated:
        return redirect("/home")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = UserCreationForm()

    context = {"form": form}
    return HttpResponse(template.render(context, request))
