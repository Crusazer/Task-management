from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import Employee, Customer
from users.serializers import (
    RegisterEmployeeSerializer,
    RegisterCustomerSerializer,
    UserSerializer
)

User = get_user_model()


# Create your views here.
class RegisterEmployeeView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = RegisterEmployeeSerializer
    permission_classes = [permissions.AllowAny]


class RegisterCustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
