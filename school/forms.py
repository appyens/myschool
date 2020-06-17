from django import forms

from .models import Standard
from account.models import Profile


class AddStandardForm(forms.ModelForm):

    class Meta:
        model = Standard
        fields = ('standard', 'max_students')


class AddClassTeacherForm(forms.ModelForm):

    def __init__(self):
        super().__init__()
        self.fields['teacher'] = Profile.objects.teachers()
        self.fields['standard'] = Standard.objects.filter(is_active=True)
