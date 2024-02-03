# Generated by Django 4.2.3 on 2024-02-02 05:38

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app322', '0011_alter_tender_tender_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyregistration',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='companyregistration',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='groups',
            field=models.ManyToManyField(related_name='company_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='user_permissions',
            field=models.ManyToManyField(related_name='company_user_permissions', to='auth.permission'),
        ),
        migrations.AddField(
            model_name='companyregistration',
            name='username',
            field=models.CharField(default='', max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='companyregistration',
            name='company_name',
            field=models.CharField(default=0, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='companyregistration',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='companyregistration',
            name='vat_registration_number',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
