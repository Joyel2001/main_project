# Generated by Django 4.2.3 on 2023-08-30 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0027_alter_bin_image_binbooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='binbooking',
            name='name',
        ),
    ]
