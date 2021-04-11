from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# /
@login_required(login_url='/login/')
def blank_view(request):
    if request.user.is_authenticated:
        return redirect("/home")

    return redirect("/login")
