# Generated by Django 4.2.3 on 2023-08-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0023_bin'),
    ]

    operations = [
        migrations.AddField(
            model_name='bin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bin_images/'),
        ),
    ]
