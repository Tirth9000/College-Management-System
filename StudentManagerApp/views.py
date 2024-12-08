from django.shortcuts import render, redirect
from auth_app.models import UserModel, StudentDatabase
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from StudentManagerApp.models import *


# Create your views here.
def StudentHome(request, id):
    user = UserModel.objects.get(user_id = id)
    student = StudentDatabase.objects.get(student = user)
    age = student.calculate_age()
    return render(request, 'student_home.html', {'student': student, 'age': age}) 

def AdminHome(request, id):
    student = StudentDatabase.objects.get(student = UserModel.objects.get(user_id = id))
    total_banches = '3'
    total_students = UserModel.objects.filter(is_staff=False).count()
    total_faculties = UserModel.objects.filter(is_staff=True).count()
    data = {'total_branches': total_banches, 'total_students': total_students, 'total_faculties': total_faculties}
    return render(request, 'admin_page.html', {'data': data, 'student': student})

def Logout(request):
    logout(request)
    return render(request, 'landing-register.html')


def StudentServices(request, id):
    return render(request, 'services.html')


def StudentAbout(request, id):
    return render(request, 'about.html')

def StudentContact(request, id):
    return render(request, 'contact.html')

def AdminAbout(request, id):
    return render(request, 'admin_about.html')

def AdminContact(request, id):
    return render(request, 'admin_contact.html')


def AllStudents(request, id):
    print('hello')
    branch = request.GET.get('branch')
    if branch:
        print('world')
        students = StudentDatabase.objects.filter(branch=branch)
    else:
        students = StudentDatabase.objects.filter(student__is_staff=False)
    return render(request, 'all_students.html', {'students': students})

def UpdateStudent(request, id, std_id):
    user = UserModel.objects.get(user_id = std_id)
    student = StudentDatabase.objects.get(student=user)
    
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student.email = request.POST.get('email')

        if request.POST.get('dob') is not None:
            student.dob = request.POST.get('dob')

        if request.POST.get('branch') != 'Select':
            print(request.POST.get('branch'))
            student.branch = request.POST.get('branch')

        if request.POST.get('gender') != 'Select':
            print(request.POST.get('gender'))
            student.gender = request.POST.get('gender')
        
        if request.FILES.get('image_pic') is not None:
            student.image = request.FILES.get('image_pic')

        if request.FILES.get('sign_pic') is not None:
            student.sign = request.FILES.get('sign_pic')
        
        student.save()
        return redirect('all_students', id=id)
    return render(request, 'update_student.html', {'student': student})


def DeleteStudent(request, id, std_id):
    user = UserModel.objects.get(user_id = std_id)
    # student = StudentDatabase.objects.get(student=user)
    user.delete()
    return redirect('all_students', id=id)

    
def FilterBy(request, id):
    print('world')
    branch = request.GET.get('branch')
    if branch:
        students = StudentDatabase.objects.filter(branch=branch)
    else:
        students = StudentDatabase.objects.all()
    return render(request, 'all_students.html', {'students': students})

    
    