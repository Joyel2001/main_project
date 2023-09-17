# Generated by Django 4.2.3 on 2023-09-14 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0051_binbooking_booking_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_level', models.IntegerField(choices=[(20, '20%'), (40, '40%'), (50, '50%'), (70, '70%'), (90, '90%')])),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app32.binbooking')),
            ],
        ),
    ]
