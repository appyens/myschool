from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from school.models import Standard, Address, Religion, CastCategory, Language
from .manager import ProfileManager


class Profile(models.Model):
    """
    User profile model
    """
    PROFILE_CHOICE = (
        ('personal', 'Personal'),
        ('professional', 'Professional'),
    )
    ROLE_CHOICE = (
        ('headmaster', 'Headmaster'),
        ('teacher', 'Teacher'),
        ('non_teacher', 'Non Teacher'),
    )
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=128, choices=GENDER_CHOICE, blank=True)
    role = models.CharField(max_length=128, choices=ROLE_CHOICE, blank=True)
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True)
    photo = models.ImageField(upload_to='account/staff/', blank=True)
    standard = models.OneToOneField(Standard, on_delete=models.DO_NOTHING, blank=True, null=True)
    uid = models.CharField(max_length=12, blank=True)
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    cast = models.CharField(max_length=512)
    religion = models.ForeignKey(Religion, on_delete=models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(CastCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, blank=True, null=True)
    # qualification
    # experience
    # school history
    # date_joined
    # training attended
    is_teacher = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user.username)

    def clean(self):
        if self.role == 'non_teacher' and self.standard:
            raise ValidationError("Non teaching staff cannot have standard")

    def is_teacher(self):
        if (self.role == 'teacher' or 'head_master') and self.standard:
            return True

    def get_age(self):
        pass


class ClassTeacher(models.Model):
    """
    Teacher is attached with one standard
    """
    teacher = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    standard = models.ForeignKey(Standard, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.teacher.user.get_full_name() + ' - ' + self.standard.standard)


# signal
def add_profile_signal(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


post_save.connect(add_profile_signal, sender=User)
