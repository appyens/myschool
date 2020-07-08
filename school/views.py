from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ClusterForm, SchoolForm, StandardForm, ClassTeacherForm, StudentForm, CreateStaffForm
from .models import Standard, School
from common.decorators import headmaster_required
from account.models import Profile


@headmaster_required
def setup_school(request):
    if request.method == 'POST':
        cluster_form = ClusterForm(data=request.POST)
        school_form = SchoolForm(data=request.POST)
        if cluster_form.is_valid() and school_form.is_valid():
            cluster = cluster_form.save()
            school = school_form.save(commit=False)
            school.cluster = cluster
            school.save()
            for i in range(1, school.max_standards + 1):
                Standard.objects.create(school=school, standard=i)
            messages.success(request, "")
            cluster_form = ClusterForm()
            school_form = SchoolForm()
            return render(request, 'school/setup-school.html', {'cluster_form': cluster_form, 'school_form': school_form})
        else:
            cluster_form = ClusterForm(data=request.POST)
            school_form = SchoolForm(data=request.POST)
            return render(request, 'school/setup-school.html', {'cluster_form': cluster_form, 'school_form': school_form})
    cluster_form = ClusterForm()
    school_form = SchoolForm()
    return render(request, 'school/setup-school.html', {'cluster_form': cluster_form, 'school_form': school_form})


def create_staff(request):
    if request.method == 'POST':
        user_form = CreateStaffForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            user = user_form.save(commit=False)
            username = user.username
            password = User.objects.make_random_password()
            user.set_password(password)
            # send mail
            login_url = request.build_absolute_uri(reverse('account:login'))
            subject = "You are registered with myschool"
            message = """
            Hello %s You are registered with Myschool
            Here is your credential
            username: %s
            Password: %s
            Use this %s to login and start managing your class
            """ % (user.first_name, username, password, login_url)
            user.email_user(subject=subject, message=message)
            user.save()
            user_form = CreateStaffForm()
            return render(request, 'school/create-staff.html', {'user_form': user_form})
    user_form = CreateStaffForm()
    return render(request, 'school/create-staff.html', {'user_form': user_form})


@headmaster_required
def add_class_teacher(request):
    if request.method == 'POST':
        form = ClassTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data.get('teacher')
            standard = form.cleaned_data.get('standard')
            profile = Profile.objects.get(user__username=teacher)
            standard = Standard.objects.get(standard=standard)
            profile.standard = standard
            profile.save()
            messages.success(request, "Class added successfully")
            form = ClassTeacherForm()
            return render(request, 'school/add-class-teacher.html', {'form': form})
    form = ClassTeacherForm()
    return render(request, 'school/add-class-teacher.html', {'form': form})


def add_student(request):
    if request.method == 'POST':
        st = {'first_name': "VIlas", 'last_name': 'Nevkar'}
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully")
            return render(request, 'manage/add-student.html', {})
    form = StudentForm()
    return render(request, 'manage/add-student.html', {'form': form})
