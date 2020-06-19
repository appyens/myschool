from django.shortcuts import render, reverse, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import UserRegisterForm, UserLoginForm, EditProfileForm, AddStandardForm, AddClassTeacherForm
from .models import Profile, ClassTeacher

from common.decorators import headmaster_required


User = get_user_model()


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


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
            # Profile.objects.create(user=new_user)
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
def show_profile(request, username=None):
    template = 'account/show_profile.html'
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    can_edit = False
    if request.user.profile.role == 'headmaster' and username == request.user.username:
        can_edit = True
    return render(request, template_name=template, context={'profile': profile, 'can_edit': can_edit})


def edit_profile(request):
    template = 'account/edit_profile.html'
    if request.method == 'POST':
        form = EditProfileForm(instance=Profile.objects.get(user=request.user), data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:show_profile')
    initial_data = Profile.objects.filter(user=request.user).values()[0]
    form = EditProfileForm(initial=initial_data)
    return render(request, template_name=template, context={'form': form})


@login_required
@headmaster_required
def staff_list(request):
    template = 'manage/staff-list.html'
    total_staff = Profile.objects.filter(is_active=True).exclude(user=request.user)
    return render(request, template_name=template, context={'staff': total_staff})


@headmaster_required
def add_standard(request):
    if request.method == 'POST':
        form = AddStandardForm(data=request.POST)
        if form.is_valid():
            standard = form.save(commit=False)
            standard.school_id = 1
            standard.save()
            messages.success(request, "Class added successfully")
            return render(request, 'manage/add-standard.html', {})
        else:
            form = AddStandardForm()
            return render(request, 'manage/add-standard.html', {'form': form})
    form = AddStandardForm()
    return render(request, 'manage/add-standard.html', {'form': form})


@headmaster_required
def add_class_teacher(request):
    if request.method == 'POST':
        form = AddClassTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class added successfully")
            return render(request, 'manage/add-class-teacher.html', {})
    form = AddClassTeacherForm()
    return render(request, 'manage/add-class-teacher.html', {'form': form})


@headmaster_required
def class_list(request):
    items = ClassTeacher.objects.all()
    return render(request, 'manage/class-list.html', {'items': items})