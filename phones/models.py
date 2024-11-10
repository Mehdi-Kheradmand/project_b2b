from django.db import models
from rest_framework.exceptions import ValidationError
from utils.validate_utils import is_iran_mobile


def validate_charge_balance(value):
    if value < 0:
        raise ValidationError("Credit balance cannot be negative.")
    if value > 999999999999:
        raise ValidationError("Credit balance cannot be more than 999,999,999,999.")
    return value


def validate_phone_number(value):
    if is_iran_mobile(value):
        return value
    raise ValidationError("Invalid PhoneNumber")


class Phone(models.Model):
    number = models.CharField(
        unique=True, max_length=11, verbose_name="Phone Number", validators=[validate_phone_number])
    charge_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[validate_charge_balance])

    def __str__(self):
        return self.number
