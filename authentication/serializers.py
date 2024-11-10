from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    date_joined = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    credit_balance = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=15)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_active', 'is_staff', 'last_login']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data: dict) -> User:
        new_user = User.objects.create(**validated_data)
        new_user.set_password(validated_data.get("password"))
        new_user.save()
        return new_user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_active', 'is_staff']
        read_only_fields = [
            'email',
            'date_joined',
            'is_superuser',
            'credit_balance',
            'first_name',
            'last_name', 'last_login']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
