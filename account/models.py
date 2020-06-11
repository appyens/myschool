from django.db import models
from django.contrib.auth.models import User
from school.models import Standard


class StaffRole(models.Model):
    role = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.role


class StaffProfile(models.Model):
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=128, choices=GENDER_CHOICE, blank=True)
    uid = models.CharField(max_length=12, blank=True)
    dob = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='account/staff/', blank=True)
    role = models.ForeignKey(StaffRole, on_delete=models.DO_NOTHING, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.username)


class Teacher(StaffProfile):
    standard = models.OneToOneField(to=Standard, on_delete=models.DO_NOTHING, blank=True, null=True)
    qualification = models.CharField(max_length=10)
    date_joined = models.DateField(blank=True, null=True)


class NonTeacher(StaffProfile):
    qualification = models.CharField(max_length=10)
    date_joined = models.DateField(blank=True, null=True)
