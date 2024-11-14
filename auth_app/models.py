from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils import timezone


# Create your models here.
class CustomUserModel(BaseUserManager):
    def create_user(self, user_id, email=None, password=None):
        if not user_id:
            raise ValueError('Admin id must required!')
        user = self.model(
            user_id = user_id,
            email = email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None):
        user = self.create_user(
            user_id=user_id,
            password=password,
        )
        user.email='tirth@gmail.com'
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    
class UserModel(AbstractBaseUser):
    user_id = models.CharField(max_length=6, primary_key=True, default=None)
    email = models.EmailField(max_length=30, null=True)
    password = models.CharField(max_length=200)
    is_staff = models.BooleanField(verbose_name='isStaff', default=False)
    is_active = models.BooleanField(verbose_name='isActive', default=True)
    is_superuser = models.BooleanField(verbose_name='isSuperuser', default=False)

    objects = CustomUserModel()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []
      
    def __str__(self):
        return self.user_id
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_staff

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(UserModel, self).save(*args, **kwargs)


class StudentDatabase(models.Model):  
    # create drop-down for the selected branches
    SELECT_BRANCH = [
        ('select', 'Select'),
        ('B.Tech/CSE', 'B.Tech/CSE'),
        ('B.Tech/FEHS', 'B.Tech/FEHS'),
        ('B.Tech/Chemical', 'B.Tech/Chemical')
    ]

    SELECT_GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    ]
    student = models.OneToOneField(UserModel, primary_key=True, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    gender = models.CharField(max_length = 1, choices=SELECT_GENDER, null = True)
    dob = models.DateField(default = timezone.now)
    branch = models.CharField(max_length = 50, choices=SELECT_BRANCH, default='select')
    image = models.FileField(upload_to = 'StudentImage/', default = None, blank = True)
    sign = models.FileField(upload_to = 'StudentSign/', default = None, blank = True)

    # calculate age for today
    def calculate_age(self: object) -> int:
        today = timezone.now().date()  # Get the current date
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    
    def __str__(self):
        return self.student.user_id


# authenticate the user 
# def user_authenticate(userid: str, password: str) -> object:
#     user = StudentDatabase.objects.filter(id=userid)
#     if user and check_password(password, user[0].password):
#         return user
#     return None

    
# check the password having the constraints or not 
# return False if password is valid
def CheckPasswordConstraits(password: str)-> bool:
    special_char = ['/', '[', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', ':', '{', '}', '|', '<', '>', ']']
    if len(password) < 8:
        return True
    elif " " in password.strip():
        return True
    else:
        upper_flag = 0
        lower_flag = 0
        digit_flag = 0
        special_flag = 0
        for char in password:
            if char in special_char:
                special_flag += 1
                continue
            elif char.isdigit():
                digit_flag += 1
                continue
            elif char.islower():
                lower_flag += 1
                continue
            elif char.isupper():
                upper_flag += 1
                continue
            else:
                continue
            
        if (upper_flag == 0 or lower_flag == 0) or (digit_flag == 0 or special_flag == 0):
            return True
    return False

