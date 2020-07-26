from django import forms
from school.models import Standard


class ReportForm(forms.Form):
    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    standard = forms.ModelChoiceField(queryset=Standard.objects.all())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
