# Generated by Django 4.2.3 on 2023-08-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0010_event_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('street', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('number_of_attendees', models.PositiveIntegerField()),
            ],
        ),
    ]
