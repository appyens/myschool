import csv

from django.http import HttpResponse
from django.shortcuts import render

from school.models import Student, Standard

from .forms import ReportForm

# Create your views here.


def student_reports(request):

    form = ReportForm(request.GET)
    if form.is_valid():
        std = form.cleaned_data.get('standard')
        gender = form.cleaned_data.get('gender')
        std = Standard.objects.get(standard=std)
        students = Student.objects.filter(standard=std, gender=gender)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="standard_%s_students.csv"' % std.standard
        writer = csv.writer(response)
        writer.writerow("Sr/No,standard,grn,student_id,uid,first_name,middle_name,last_name,dob,gender,religion,cast,category".split(','))
        for index, item in enumerate(students, start=1):
            writer.writerow([index, item.standard, item.grn, item.student_id, item.uid, item.first_name, item.middle_name, item.last_name, item.dob, item.gender, item.religion, item.cast, item.category])
        return response

    return render(request, 'report.html', {'form': form})
