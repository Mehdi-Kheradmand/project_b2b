from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError

from phones.models import Phone


def validate_amount(value):
    if value < 0:
        raise ValidationError("Amount cannot be negative.")
    if value > 999999999999:
        raise ValidationError("Amount cannot be more than 999,999,999,999.")
    return value


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_amount])
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.seller} - {self.transaction_type} - {self.amount}"

    class Meta:
        ordering = ['-created_at']


class CreditRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_amount])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_requests'
    )

    def __str__(self):
        return f"{self.seller} - {self.amount} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class RechargeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_amount])
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.seller} - {self.phone} - {self.amount} - {self.status}"
