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

from BlackboardCompanion import views as baseViews
from BlackboardCompanion import settings
from Enrolled_Classes import views as classesView

urlpatterns = [
    path('', views.blank_view),
    path('home/', baseViews.home_view),
    path('admin/', admin.site.urls),
    path('login/', baseViews.login_view),
    path('register/', baseViews.register_view)
    path('enrolled-classes'), classesView.enrolledClasses_view),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
