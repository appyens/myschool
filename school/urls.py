from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('setup/', views.setup_school, name='setup'),
    path('staff/add/', views.create_staff, name='create_staff'),
    path('staff/class/add/', views.add_class_teacher, name='add_class_teacher'),
]