# Generated by Django 5.1.3 on 2024-11-09 10:00

import phones.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=11, unique=True, validators=[phones.models.validate_phone_number], verbose_name='Phone Number')),
                ('charge_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[phones.models.validate_charge_balance])),
            ],
        ),
    ]