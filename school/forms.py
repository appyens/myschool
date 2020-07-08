from django import forms

from .models import Standard, Student, Cluster, School
from account.models import Profile
from django.contrib.auth.models import User
from .models import Religion


class ClusterForm(forms.ModelForm):

    class Meta:
        model = Cluster
        fields = ('name',)
        labels = {'name': 'Cluster name'}


class SchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = ('name', 'place', 'academic_year', 'max_standards', 'max_staff')
        labels = {
            'name': 'School Name',
        }


class CountInputForm(forms.Form):
    count = forms.IntegerField()


class CreateStaffForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'id': 'inputFirstName',
        'placeholder': 'Enter first name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'id': 'inputLastName',
        'placeholder': 'Enter last name',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'id': 'inputUsername',
        'placeholder': 'Enter username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'id': 'inputEmailAddress',
        'aria-describedby': 'emailHelp',
        'placeholder': 'Enter email address',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class StandardForm(forms.ModelForm):

    class Meta:
        model = Standard
        fields = ('standard',)


class ClassTeacherForm(forms.Form):

    teacher = forms.ChoiceField(
        widget=forms.Select,
        choices=((i, i) for i in Profile.objects.all().values_list('user__username', flat=True)),
    )
    standard = forms.ChoiceField(
        widget=forms.Select,
        choices=((i, i) for i in Standard.objects.all().values_list('standard', flat=True)))


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['religion'].queryset = Religion.objects.filter(name__startswith='A')
        self.fields['first_name'].initial = "khdsf"
