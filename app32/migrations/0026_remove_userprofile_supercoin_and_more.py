# Generated by Django 4.2.3 on 2024-03-12 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0025_alter_userprofile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='supercoin',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
