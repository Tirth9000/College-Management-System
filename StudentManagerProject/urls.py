"""
URL configuration for StudentManagerProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_app.views import *
from StudentManagerApp.views import *
from StudentManagerProject import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageWithRegistration, name='landing_register'),
    path('login-page/', UserLogin, name='login_page'),
    path('student-home/<str:id>/', StudentHome, name='student_home_page'),
    path('student-home/<str:id>/home/', StudentHome, name='student_home_page'),
    path('student-home/<str:id>/about/', StudentAbout, name='student_about_page'),
    path('student-home/<str:id>/contact/', StudentContact, name='student_contact_page'),
    path('admin-home/<str:id>/', AdminHome, name='admin_home'),
    path('admin-home/<str:id>/home/', AdminHome, name='admin_home_page'),
    path('admin-home/<str:id>/about/', AdminAbout, name='admin_about_page'),
    path('admin-home/<str:id>/contact/', AdminContact, name='admin_contact_page'),
    
    path('admin-home/<str:id>/all-students/', AllStudents, name='all_students'),
    path('admin-home/<str:id>/all-students/', FilterBy, name='filter_by'),
    path('admin-home/<str:id>/all-students/update-student/<str:std_id>/', UpdateStudent, name='update_student'),
    path('admin-home/<str:id>/all-students/delete-student/<str:std_id>/', DeleteStudent, name='delete_student'),

    path('logout/', Logout, name='logout'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
