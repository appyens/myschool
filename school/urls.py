from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('standard/add/', views.create_standard, name='add_standard'),
    path('class-teacher/add/', views.add_class_teacher, name='add_class_teacher'),
]