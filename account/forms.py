from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import StaffProfile

USERNAME = r'^[A-Za-z0-9_-]+$'


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

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
        model = StaffProfile
        fields = ('gender', 'uid', 'dob', 'photo', 'address', 'mobile')