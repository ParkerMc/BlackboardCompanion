"""BlackboardCompanion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from BlackboardCompanion import views as base_views
from BlackboardCompanion import settings
from Enrolled_Classes import views as classes_views
from User_Management import views as user_views

urlpatterns = [
    path('', base_views.blank_view),
    path('home/', base_views.home_view),
    path('admin/', admin.site.urls),
    path('login/', user_views.login_view),
    path('register/', user_views.register_view),
    path('enrolled-classes/', classes_views.enrolledClasses_view),
    path('qr-reader', base_views.qr_reader)

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
