from django.contrib import admin
from .models import StaffProfile, StaffRole, NonTeacher, Teacher

admin.site.register(StaffRole)
admin.site.register(StaffProfile)
admin.site.register(NonTeacher)
admin.site.register(Teacher)