# Generated by Django 4.2.3 on 2024-03-12 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app32', '0022_alter_supercoin_coins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supercoin',
            name='coins',
            field=models.IntegerField(default=None),
        ),
    ]
