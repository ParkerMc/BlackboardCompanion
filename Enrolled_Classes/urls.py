from .views import class_view, class_delete, add_class_view
from django.urls import path

app_name = 'Enrolled_Classes'

urlpatterns = [
    path('<int:pk>/delete/', class_delete, name='class_delete'),
    path('', class_view, name='classes'),
    path('add/', add_class_view, name='class_add'),
]
