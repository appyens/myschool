from django.urls import reverse
from django.db import models
from django.core.exceptions import ValidationError


class School(models.Model):
    cluster = models.CharField(max_length=128)
    name = models.CharField(max_length=512)
    place = models.CharField(max_length=256)
    academic_year = models.CharField(max_length=32)
    max_standards = models.PositiveIntegerField()
    max_staff = models.PositiveIntegerField()
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
    standard = models.CharField(max_length=1, unique=True)
    max_students = models.PositiveIntegerField(blank=True, null=True)
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

    def clean(self):
        try:
            if isinstance(int(str(self.standard)), int):
                return self.standard
        except ValueError:
            raise ValidationError("please provide valid number")


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


class Student(models.Model):

    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    standard = models.ForeignKey(to=Standard, on_delete=models.DO_NOTHING, related_name='students')
    grn = models.IntegerField(unique=True)
    # unique = True, Integer
    student_id = models.CharField(max_length=19)
    uid = models.CharField(max_length=12, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    dob = models.DateField()
    gender = models.CharField(max_length=8, choices=GENDER_CHOICE)
    religion = models.ForeignKey(Religion, on_delete=models.DO_NOTHING)
    cast = models.CharField(max_length=256)
    category = models.ForeignKey(CastCategory, on_delete=models.DO_NOTHING)
    mother_tongue = models.ForeignKey(Language, on_delete=models.DO_NOTHING, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    address = models.ManyToManyField(Address, blank=True)
    mother_first_name = models.CharField(max_length=256, blank=True, null=True)
    father_middle_name = models.CharField(max_length=256, blank=True, null=True)
    nationality = models.CharField(max_length=256, default='Indian')
    photo = models.ImageField(upload_to='student/%Y/%m/%d/', null=True, blank=True)
    last_school = models.CharField(max_length=256, blank=True, null=True)
    admitted_std = models.OneToOneField(Standard, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return full_name

    def get_absolute_url(self):
        return reverse('school:student_detail', args=[self.grn])

    @classmethod
    def total_students(cls):
        students = cls.objects.filter(is_active=True).count()
        return students

