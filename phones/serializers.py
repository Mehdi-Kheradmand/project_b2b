from rest_framework import serializers
from .models import Phone
from utils.validate_utils import is_iran_mobile


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = '__all__'
        read_only_fields = ['charge_balance']

    @staticmethod
    def validate_number(value):
        if is_iran_mobile(value):
            return value
        raise serializers.ValidationError("Invalid Phone Number")
