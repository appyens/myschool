from django.shortcuts import render, reverse, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.apps import apps

from .forms import UserRegisterForm, UserLoginForm, EditProfileForm
from .models import Profile


User = get_user_model()


@login_required
def dashboard(request):
    """
    A login redirect view
    :param request:
    :return:
    """
    total_staff = Profile.objects.count()
    standard_model = apps.get_model('school', 'Standard')
    total_standard = standard_model.objects.count()
    student_model = apps.get_model('school.Student')
    total_student = student_model.objects.count()
    return render(request, 'account/dashboard.html', {
        'section': 'Dashboard',
        'total_staff': total_staff,
        'total_standard': total_standard,
        'total_student': total_student
    })


def staff_register(request):
    """
    Signs up to this site
    :param request:
    :return:
    """
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
    """
    User login view
    :param request:
    :return:
    """
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


@login_required
def staff_logout(request):
    """
    Logs out user from session
    :param request:
    :return:
    """
    logout(request)
    return render(request, 'registration/logout.html')


@login_required
def show_profile(request, username=None):
    """
    Show Profile model object for current user
    :param request:
    :param username:
    :return:
    """

    template = 'account/show_profile.html'
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    can_edit = False
    if request.user.profile.role == 'headmaster' and username == request.user.username:
        can_edit = True
    return render(request, template_name=template, context={'profile': profile, 'can_edit': can_edit, 'section': 'Profile'})


@login_required
def edit_profile(request):
    """
    Allows editing of current user profile
    :param request:
    :return:
    """
    template = 'account/edit_profile.html'
    if request.method == 'POST':
        form = EditProfileForm(instance=Profile.objects.get(user=request.user), data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:show_profile')
    initial_data = Profile.objects.filter(user=request.user).values()[0]
    form = EditProfileForm(initial=initial_data)
    name = request.session.get("name")
    return render(request, template_name=template, context={'form': form, 'section': 'Edit profile', "name": name})

