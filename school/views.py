from datetime import datetime

from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import SchoolForm, ClassTeacherForm, StudentForm, CreateStaffForm, UploadFileForm
from .models import Standard, Student, Religion, CastCategory
from common.decorators import headmaster_required
from account.models import Profile


@headmaster_required
def setup_school(request):
    """
    Allows setting up of school for the first time
    :param request:
    :return:
    """
    if request.method == 'POST':
        school_form = SchoolForm(data=request.POST)
        if school_form.is_valid():
            school = school_form.save(commit=False)
            school.save()
            for i in range(1, school.max_standards + 1):
                Standard.objects.create(school=school, standard=i)
            messages.success(request, "")
            school_form = SchoolForm()
            return render(request, 'school/setup-school.html', {'school_form': school_form, 'section': 'School setup'})
        else:
            return render(request, 'school/setup-school.html', {'school_form': school_form, 'section': 'School setup'})
    school_form = SchoolForm()
    return render(request, 'school/setup-school.html', {'school_form': school_form, 'section': 'School setup'})


@headmaster_required
def create_staff(request):
    """
    Creates and mail newly created staff
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = CreateStaffForm(request.POST)
        if user_form.is_valid():
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
            return render(request, 'school/create-staff.html', {'user_form': user_form, 'section': 'Add staff'})
        else:
            return render(request, 'school/create-staff.html', {'user_form': user_form, 'section': 'Add staff'})
    user_form = CreateStaffForm()
    return render(request, 'school/create-staff.html', {'user_form': user_form, 'section': 'Add staff'})


@headmaster_required
def add_class_teacher(request):
    """
    Assigns class to the teacher
    :param request:
    :return:
    """
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
            return render(request, 'school/add-class-teacher.html', {'form': form, 'section': 'Add class-teacher'})
    form = ClassTeacherForm()
    return render(request, 'school/add-class-teacher.html', {'form': form, 'section': 'Add class-teacher'})


@headmaster_required
def staff_list(request):
    """
    All staff list
    :param request:
    :return:
    """
    template = 'account/staff-list.html'
    total_staff = Profile.objects.filter(is_active=True)
    return render(request, template_name=template, context={'staff': total_staff, 'section': 'All staff'})


def standard_list(request):
    """
    All standard list
    :param request:
    :return:
    """
    standards = Standard.objects.all()
    return render(request, 'school/standard-list.html', {'standards': standards, 'section': 'All classes'})


def my_class(request):
    """
    If user has class associated with him/her, then it show class overview
    :param request:
    :return:
    """
    profile = Profile.objects.get(user=request.user)
    return render(request, 'school/my-class.html', {'profile': profile, 'section': 'My class'})


def class_detail(request, std_number):
    """
    Display student list in the class
    :param request:
    :param std_number:
    :return:
    """
    std = Standard.objects.get(standard=std_number)
    students = Student.objects.filter(standard=std)
    return render(request, 'school/class-detail.html', {'students': students, 'section': 'My class'})


def add_student(request):
    """
    Allows adding student individually with form or upload student list with csv file.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        file_form = UploadFileForm(request.POST, request.FILES)

        if file_form.is_valid():
            file = file_form.cleaned_data['file']
            file_data = file.read().decode("utf-8")
            lines = file_data.split("\n")
            # FIXME: lopping for one extra time

            for line in lines[1:]:
                data = line.split(',')
                date = list(map(int, data[8].split('/')))
                std = Standard.objects.get(standard=data[1])
                religion = Religion.objects.get(name=data[10])
                category = CastCategory.objects.get(category=data[12].strip())
                student = Student.objects.create(
                    standard=std,
                    grn=int(data[2]),
                    student_id=data[3],
                    uid=data[4],
                    first_name=data[5],
                    middle_name=data[6],
                    last_name=data[7],
                    dob=datetime(year=date[2], month=date[1], day=date[0]),
                    gender=data[9],
                    religion=religion,
                    cast=data[11],
                    category=category
                )
                student.save()

        elif form.is_valid():
            student = form.save(commit=False)
            student.save()
            messages.success(request, "Student added successfully")
            return render(request, 'school/add-student.html', {})
        else:
            return render(request, 'school/add-student.html', {'form': form, 'file_form': file_form, 'section': 'Add student'})
    form = StudentForm()
    file_form = UploadFileForm()
    return render(request, 'school/add-student.html', {'form': form, 'file_form': file_form, 'section': 'Add student'})


def student_detail(request):
    pass


def download_csv(request):
    pass

