# Generated by Django 4.2.3 on 2023-09-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0050_remove_binbooking_address_remove_binbooking_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='binbooking',
            name='booking_id',
            field=models.CharField(default=None, max_length=5),
        ),
    ]
