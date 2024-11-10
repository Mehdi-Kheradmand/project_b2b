# Generated by Django 5.1.3 on 2024-11-10 17:47

import accounting.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('phones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[accounting.models.validate_amount])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_requests', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RechargeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[accounting.models.validate_amount])),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processed', 'Processed'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('phone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='phones.phone')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[accounting.models.validate_amount])),
                ('transaction_type', models.CharField(choices=[('increase', 'Increase'), ('decrease', 'Decrease')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='phones.phone')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
