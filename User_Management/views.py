from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def register_view(request):
    template = loader.get_template('User_Management/register.html')

    if request.user.is_authenticated:
        return redirect("/class")

    if request.method == "POST":
        netID = request.POST['username']
        password = request.POST['password1']
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=netID, password=password)
            if user is not None:
                login(request, user)

            return redirect('/class')
    else:
        form = UserCreationForm()

    context = {"form": form}
    return HttpResponse(template.render(context, request))


def login_view(request):
    template = loader.get_template('User_Management/login.html')

    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        netID = request.POST['netid']
        password = request.POST['password']
        user = authenticate(request, username=netID, password=password)
        if user is not None:
            login(request, user)

            if "next" in request.GET:
                return redirect(request.GET["next"])
            return redirect("/class")
        else:
            messages.error(request, "The Username and/or Password are incorrect.")

    context = {}
    return HttpResponse(template.render(context, request))
