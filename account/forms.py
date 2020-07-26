from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

from .models import Profile
from school.models import Standard, Student


USERNAME = r'^[A-Za-z0-9_-]+$'


class UserRegisterForm(forms.ModelForm):
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
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'id': 'inputPassword',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'id': 'inputConfirmPassword',
        'placeholder': 'Confirm password',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Password does not match")
        return password2


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'id': 'inputEmailAddress',
            'placeholder': 'Enter username'}),
        validators=[RegexValidator(USERNAME)]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'id': 'inputPassword',
            'placeholder': 'Enter password'
        })
    )


class EditProfileForm(forms.ModelForm):
    """"
    Profile edit form
    """

    class Meta:
        model = Profile
        fields = ('gender', 'dob', 'mobile', 'uid', 'photo', 'address', 'cast', 'religion', 'category', 'language')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': 'form-control col-5'})

