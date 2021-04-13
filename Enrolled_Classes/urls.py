from .views import class_view, class_delete, add_class_view
from django.urls import path

app_name = 'Enrolled_Classes'

urlpatterns = [
    path(r'^delete/(?P<pk>[0-9]+)/$', class_delete, name='class_delete'),
    path('', class_view, name='classes'),
    path('add/', add_class_view, name='add-class'),
]