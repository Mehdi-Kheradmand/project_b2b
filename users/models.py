from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import permissions
from rest_framework.exceptions import ValidationError


def validate_credit_balance(value):
    if value < 0:
        raise ValidationError("Credit balance cannot be negative.")
    if value > 1000000:
        raise ValidationError("Credit balance cannot be more than 999,999,999,999,999.")
    return value


# Create your models here.
class User(AbstractUser):
    credit_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, validators=[validate_credit_balance])

    def __str__(self):
        return f"{self.username} - Credit: {self.credit_balance}"


# permissions
class IsAuthenticatedAndSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        the_user: User = request.user
        return the_user.is_authenticated and the_user.is_superuser
