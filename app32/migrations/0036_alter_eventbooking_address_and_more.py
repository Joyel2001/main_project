# Generated by Django 4.2.3 on 2023-09-02 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app32', '0035_eventbooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventbooking',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='eventbooking',
            name='booking_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='eventbooking',
            name='event',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app32.event'),
        ),
        migrations.AlterField(
            model_name='eventbooking',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
