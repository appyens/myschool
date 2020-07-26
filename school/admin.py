from django.contrib import admin
from .models import Standard, School, Language, CastCategory, Scheme, Religion, Address, Student

admin.site.register(Standard)
admin.site.register(School)
admin.site.register(Language)
admin.site.register(CastCategory)
admin.site.register(Scheme)
admin.site.register(Religion)
admin.site.register(Address)


class StudentAdmin(admin.ModelAdmin):

    list_display = ['full_name', 'standard', 'gender']


admin.site.register(Student, StudentAdmin)