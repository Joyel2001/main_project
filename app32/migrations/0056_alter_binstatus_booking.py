# Generated by Django 4.2.3 on 2023-09-14 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0055_alter_binstatus_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binstatus',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app32.binbooking'),
        ),
    ]
