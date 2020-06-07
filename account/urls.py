from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.staff_register, name='register'),
    path('login/', views.staff_login, name='login'),

]
