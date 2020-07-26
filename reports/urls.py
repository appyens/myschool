from django.urls import path
from . import views


app_name = 'reports'

urlpatterns = [
    path('student/', views.student_reports, name='student_report')
]