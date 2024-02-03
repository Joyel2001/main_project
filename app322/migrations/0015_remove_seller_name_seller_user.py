# Generated by Django 4.2.3 on 2024-02-03 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app322', '0014_rename_company_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='name',
        ),
        migrations.AddField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
