from django.db import models
from django.shortcuts import reverse

from school.models import Religion, CastCategory, Language, Standard


class StudentModel(models.Model):

    GENDER_CHOICE = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    standard = models.ForeignKey(to=Standard, on_delete=models.DO_NOTHING)
    grn = models.IntegerField(primary_key=True)
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
    mother_tongue = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    admission_date = models.DateField()
    mother_first_name = models.CharField(max_length=256, blank=True, null=True)
    father_middle_name = models.CharField(max_length=256, blank=True, null=True)
    nationality = models.CharField(max_length=256, default='Indian')
    photo = models.ImageField(upload_to='student/%Y/%m/%d/', null=True, blank=True)
    last_school = models.CharField(max_length=256, blank=True, null=True)
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
        return reverse('students:student_detail', args=[self.grn])

    @classmethod
    def total_students(cls):
        students = cls.objects.filter(is_active=True).count()
        return students

