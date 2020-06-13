from django.shortcuts import render, reverse, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserLoginForm, EditProfileForm
from .models import Profile

from student.models import StudentModel
from common.decorators import headmaster_required


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def staff_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        print(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the user object
            new_user.save()
            # create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'registration/registration_done.html', {'new_user': new_user})
    else:
        user_form = UserRegisterForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


def staff_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('account:dashboard'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form': form})


def staff_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')


@login_required
def show_profile(request):
    template = 'account/show_profile.html'
    profile = Profile.objects.get(user=request.user)
    return render(request, template_name=template, context={'profile': profile})


def edit_profile(request):
    template = 'account/edit_profile.html'
    context = {}
    if request.method == 'POST':
        form = EditProfileForm(request, instance=Profile.objects.get(user=request.user), data=request.POST)
        if form.is_valid():
            form.save()
            form = EditProfileForm(request)
            context['edit_form'] = form
            return redirect('account:show_profile')
    form = EditProfileForm(request)
    context['edit_form'] = form
    return render(request, template_name=template, context=context)


@login_required
@headmaster_required
def all_staff(request):
    template = 'account/staff.html'
    total_staff = Profile.objects.filter(is_active=True).exclude(user=request.user)

    return render(request, template_name=template, context={'staff': total_staff})


@headmaster_required
def all_students(request):
    students = StudentModel.objects.filter(is_active=True)
