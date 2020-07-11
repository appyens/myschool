from django import forms

from .models import Standard, Student, School
from account.models import Profile
from django.contrib.auth.models import User


class SchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = ('name', 'place', 'academic_year', 'max_standards', 'max_staff')
        labels = {
            'name': 'School Name',
        }

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control'})


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

    def __init__(self, *args, **kwargs):
        super(CreateStaffForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StandardForm(forms.ModelForm):

    class Meta:
        model = Standard
        fields = ('standard',)

    def __init__(self, *args, **kwargs):
        super(StandardForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ClassTeacherForm(forms.Form):

    teacher = forms.ChoiceField(
        widget=forms.Select,
        choices=((i, i) for i in Profile.objects.all().values_list('user__username', flat=True)),
    )
    standard = forms.ChoiceField(
        widget=forms.Select,
        choices=((i, i) for i in Standard.objects.all().values_list('standard', flat=True)))

    def __init__(self, *args, **kwargs):
        super(ClassTeacherForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UploadFileForm(forms.Form):

    file = forms.FileField(help_text="Select CSV file only")

    def clean_file(self):
        file = self.cleaned_data.get('file')
        allowed_ext = ['csv', 'CSV']
        file_name, extension = file.name.split('.')
        if extension not in allowed_ext:
            raise forms.ValidationError("Wrong file type, try again")
        return file

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control'})
