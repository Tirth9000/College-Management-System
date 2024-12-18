# Generated by Django 5.1 on 2024-10-25 13:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(default=None, max_length=6, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=30, null=True)),
                ('password', models.CharField(max_length=200)),
                ('is_staff', models.BooleanField(default=False, verbose_name='isStaff')),
                ('is_active', models.BooleanField(default=True, verbose_name='isActive')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='isSuperuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentDatabase',
            fields=[
                ('student', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1, null=True)),
                ('dob', models.DateField(default=django.utils.timezone.now)),
                ('branch', models.CharField(choices=[('select', 'Select'), ('B.Tech/CSE', 'B.Tech/CSE'), ('B.Tech/FEHS', 'B.Tech/FEHS'), ('B.Tech/Chemical', 'B.Tech/Chemical')], default='select', max_length=50)),
                ('image', models.FileField(blank=True, default=None, upload_to='StudentImage/')),
                ('sign', models.FileField(blank=True, default=None, upload_to='StudentSign/')),
            ],
        ),
    ]
