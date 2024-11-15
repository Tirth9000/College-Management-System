from django.shortcuts import redirect
from .forms import *


def user_logout(request_function):
    def inner_function(request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return redirect('login')
        except Exception:
            return request_function(request, *args, **kwargs)
        return request_function(request, *args, **kwargs)
    return inner_function

def user_login(view_function):
    def inner_function(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('')
            else: 
                return redirect('profile')
            return view_function(request, *args, **kwargs)
    return inner_function 

    