from django.shortcuts import render
from django.contrib import messages

from .models import Standard
from .forms import AddStandardForm, AddClassTeacherForm
from common.decorators import headmaster_required


@headmaster_required
def create_standard(request):
    if request.method == 'POST':
        form = AddStandardForm(data=request.POST)
        standard = form.save(commit=False)
        standard.school_id = 1
        standard.save()
        messages.success(request, "{} Class added successfully".format(standard.standard))
        return render(request, 'school/add-standard.html', {})
    form = AddStandardForm()
    return render(request, 'school/add-standard.html', {'form': form})


@headmaster_required
def add_class_teacher(request):

    if request.method == 'POST':
        form = AddClassTeacherForm()
        if form.is_valid():
            teacher = form.cleaned_data.get('teacher')
            standard = form.cleaned_data.get('standard')

        messages.success(request, "{} Class added successfully".format(standard.standard))
        return render(request, 'school/add-standard.html', {})
    form = AddStandardForm()
    return render(request, 'school/add-standard.html', {'form': form})

