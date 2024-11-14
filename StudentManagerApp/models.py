from django.db import models
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import os

# Create your models here.

# def delete(self, *args, **kwargs):
#     if self.photo:
#         if os.path.isfile(self.photo.path):
#             os.remove(self.photo.path)
#     super().delete(*args, **kwargs)