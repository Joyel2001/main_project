# Generated by Django 4.2.3 on 2024-02-11 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app322', '0025_remove_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
