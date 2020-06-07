from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import UserRegisterForm, UserLoginForm
from .models import StaffProfile


def staff_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the user object
            new_user.save()
            # create the user profile
            StaffProfile.objects.create(user=new_user)
            return render(request, 'account/registration_done.html', {'new_user': new_user})
    else:
        user_form = UserRegisterForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def staff_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Login Successful')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def staff_logout(request):
    pass