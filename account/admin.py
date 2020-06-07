from django.contrib import admin
from .models import StaffProfile, StaffRole

admin.site.register(StaffRole)
admin.site.register(StaffProfile)