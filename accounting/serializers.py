from rest_framework import serializers
from .models import Transaction, CreditRequest, RechargeRequest


# Serializer for Transactions ( every transaction that changed user's credit )
class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['seller', 'created_at']


# ---------------------------------------------------------------------


# Serializer for CreditRequests
class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ['id', 'seller', 'amount', 'status', 'created_at', 'processed_at', 'processed_by', 'description']
        read_only_fields = ['id', 'status', 'created_at', 'processed_at', 'processed_by', 'seller']

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


# Serializer for approve or reject CreditRequests by admin
class CreditRequestProcessSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=True)

    class Meta:
        model = CreditRequest
        fields = ['status']
        read_only_fields = ['id', 'seller', 'amount', 'created_at', 'processed_at', 'processed_by']

    @staticmethod
    def validate_status(value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Invalid status. Use 'approved' or 'rejected'.")
        return value


# ---------------------------------------------------------------------


# Serializer for RechargeRequests
class RechargeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RechargeRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'processed_at', 'seller', 'status']

    def validate(self, attrs):
        # validate phone
        if not attrs.get('phone'):
            raise serializers.ValidationError({"phone": "This field is required."})

        # validate amount
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError("Recharge amount must be greater than zero.")
        return attrs


# Serializer for the recharge history
class RechargeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeRequest
        fields = '__all__'
