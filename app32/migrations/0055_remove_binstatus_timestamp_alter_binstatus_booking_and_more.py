# Generated by Django 4.2.3 on 2023-09-14 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0054_binstatus_timestamp_alter_binstatus_booking_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='binstatus',
            name='timestamp',
        ),
        migrations.AlterField(
            model_name='binstatus',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app32.binbooking'),
        ),
        migrations.AlterField(
            model_name='binstatus',
            name='fill_level',
            field=models.IntegerField(choices=[(20, '20%'), (40, '40%'), (50, '50%'), (70, '70%'), (90, '90%')]),
        ),
    ]
