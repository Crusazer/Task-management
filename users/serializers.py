from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.serializerfields import PhoneNumberField

from .models import Employee, Customer

User = get_user_model()


class RegisterEmployeeSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=True)
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Employee
        fields = ('username', 'password', 'email', 'name', 'phone', 'photo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        employee = Employee(**validated_data)
        employee.set_password(validated_data['password'])
        employee.save()

        return employee

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }


class RegisterCustomerSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=True)
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Customer
        fields = ('username', 'password', 'email', 'name', 'phone', 'photo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer(**validated_data)
        customer.set_password(validated_data['password'])
        customer.save()

        return customer

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'phone', 'photo', 'role')
