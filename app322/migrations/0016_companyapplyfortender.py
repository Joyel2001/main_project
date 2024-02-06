# Generated by Django 4.2.3 on 2024-02-04 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app322', '0015_remove_seller_name_seller_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyApplyForTender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_date', models.DateField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField()),
                ('license_number', models.CharField(max_length=50)),
                ('nature_of_business', models.CharField(max_length=50)),
                ('legal_entity_type', models.CharField(max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app322.companyregistration')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app322.tender')),
            ],
        ),
    ]
