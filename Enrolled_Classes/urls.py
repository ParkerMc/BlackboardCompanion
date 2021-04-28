import Enrolled_Classes
from . import views
from .views import class_view, class_delete, add_class_view
from Attendance.views import class_settings_view
from django.urls import path
from Calendar.views import add_calendar
app_name = 'Enrolled_Classes'

urlpatterns = [
    path('<int:pk>/delete/', class_delete, name='class_delete'),
    path('<int:pk>/settings/', class_settings_view, name='class_settings_view'),
    path('', class_view, name='classes'),
    path('add/', add_class_view, name='class_add'),
    path('cal/', add_calendar, name='class_calendar'),
    #path('cal/<int:year>/<str:month>/', views.add_calendar, name='class_calendar'),

]
