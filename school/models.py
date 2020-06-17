
from django.db import models
from account.models import Profile

class Cluster(models.Model):
    name = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class School(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=512)
    place = models.CharField(max_length=256)
    academic_year = models.CharField(max_length=32)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        # set current _year
        pass


class Scheme(models.Model):
    # create separate app
    pass


class Standard(models.Model):
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    standard = models.CharField(max_length=5, unique=True)
    max_students = models.PositiveIntegerField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.standard)

    # def get_absolute_url(self):
    #     return reverse('')

    def total_classes(self):
        standards = Standard.objects.filter(is_active=True).count()
        return standards


class StandardTeacher(models.Model):
    teacher = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    standard = models.ForeignKey(Standard, on_delete=models.DO_NOTHING)


class Religion(models.Model):
    """
    1. हिंदू
    2. मुस्लिम
    3. बौद्ध
    """
    name = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    1. मराठी
    2. हिंदी
    3. बंजारी
    """
    name = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CastCategory(models.Model):
    """
        1. General
        2. SC
        3. ST
        4. OBC
        5. SBC
        6. VJ
        7. NT B
        8. NT C
        9. NT D
    """
    category = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category


class Address(models.Model):
    TYPE_CHOICE = (
        ('local', 'Local Address'),
        ('permanent', 'Permanent Address'),
    )
    type = models.CharField(max_length=512, choices=TYPE_CHOICE, default='permanent')
    line1 = models.CharField(max_length=512, blank=True)
    line2 = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=512, blank=True)
    taluka = models.CharField(max_length=512, blank=True)
    dist = models.CharField(max_length=512, blank=True)
    pin = models.CharField(max_length=6, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

