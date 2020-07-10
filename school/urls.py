from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('setup/', views.setup_school, name='setup'),
    path('staff/add/', views.create_staff, name='create_staff'),
    path('staff/class/add/', views.add_class_teacher, name='add_class_teacher'),
    path('standard/list/', views.standard_list, name='standard_list'),
    path('standard/my-class/', views.my_class, name='my_class'),
    path('standard/<int:std_number>', views.class_detail, name='class_detail'),
]