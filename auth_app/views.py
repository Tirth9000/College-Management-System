from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import random
import string
import threading
from .middlewares import *
from templates import *
from .forms import *
from .models import *
from .tasks import *


# Create your views here.
def LandingPageWithRegistration(request):
    if request.method == 'POST':
        if UserModel.objects.filter(email=request.POST.get('email')):
            messages.error(request, 'User already exist on this email!')
            return render(request, 'landing-register.html')
        else:
            userpassword = request.POST.get('password')
            if CheckPasswordConstraits(userpassword):
                messages.warning(request, 'Password Constraint invalid!')
                return render(request, 'landing-register.html') 
            else:
                NewID = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(1000, 9999))
                print(NewID)
                while UserModel.objects.filter(user_id = NewID):
                    NewID = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(1000, 9999))
                    
                user = UserModel.objects.create(
                    user_id = NewID,
                    email = request.POST.get('email'),
                )

                studentUser = StudentDatabase.objects.create(
                    student = user,
                    first_name = request.POST.get('first_name'),
                    last_name = request.POST.get('last_name'),
                    gender = request.POST.get('gender'),
                    branch = request.POST.get('branch'),
                    dob = request.POST.get('dob'),
                )
                if request.FILES.get('image_media') is not None:
                    studentUser.image = request.FILES['image_media']
                if request.FILES.get('sign_media') is not None:
                    studentUser.sign = request.FILES['sign_media']

                studentUser.student.password = make_password(userpassword)
                user.save()
                studentUser.save()
                # ConfirmationMail.delay(newuser.first_name, newuser.last_name, newuser.userID, newuser.email)
                return redirect('login_page')
    return render(request, 'landing-register.html')



@never_cache
def UserLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            user = authenticate(request, user_id=userid, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('admin_home', id = user.user_id)
                else: 
                    student = StudentDatabase.objects.get(student = user)
                    login(request, user) 
                    messages.success(request, f'{student.first_name} successfully login!')
                    return redirect('student_home_page', id = user.user_id)
            else:
                messages.error(request, 'Invalid user ID or Password!')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'from': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})



@never_cache
def ForgetPassword(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST.get('email')
            user = StudentDatabase.objects.filter(email=email)

            if user:
                request.session['user_email'] = email
                global otp
                otp = random.randint(100000, 999999)
                OTPMail.delay(otp, user[0].first_name, user[0].last_name, user[0].email)
                change_otp_timer = threading.Timer(40.0, ChangeOTP)
                change_otp_timer.start()
                return render(request, 'forget.html', {'alert': 'valid', 'otp_send': True, 'email': email})
            else:
                return render(request, 'forget.html', {'alert': 'invalid', 'email': email})
        elif 'otp' in request.POST:
            get_otp = int(request.POST.get('otp'))
            print("forget",otp)
            try:
                if otp == get_otp:
                    return redirect('reset_password')
                else:
                    return render(request, 'forget.html', {'invalid_otp': True})

            except NameError:
                return render(request, 'forget.html', {'invalid_otp': True})
    return render(request, 'forget.html')



@never_cache
def ResetPassword(request):
    if request.method == "POST":
        password = request.POST.get('new-password')
        confirmPassword = request.POST.get('confirm-password')
        if CheckPasswordConstraits(password):
            return render(request, 'reset.html', {'invalid_password': True})

        elif password != confirmPassword:
            return render(request, 'reset.html', {'confirm_password': True})

        else:
            get_user = StudentDatabase.objects.get(email=request.session.get('user_email'))
            get_user.password = make_password(password)
            get_user.save()
            request.session.pop('user_email', None)
            return redirect('login')
    return render(request, 'reset.html')


def ResendOTP(request):
    email = request.session.get('user_email')
    user = StudentDatabase.objects.get(email = email)
    global otp
    otp = random.randint(100000, 999999)
    OTPMail.delay(otp, user.first_name, user.last_name, user.email)
    change_otp_timer = threading.Timer(40.0, ChangeOTP)
    change_otp_timer.start()
    return render(request, 'forget.html', {'alert': 'valid', 'otp_send': True, 'email': email})


def UserSignout(request):
    request.session['auth_token'] = 'logout'
    request.session.pop('user', None)
    return redirect('login')





def ChangeOTP():
    global otp
    otp = 0

def error_404_view(request, exception):
    return render(request, '404.html')