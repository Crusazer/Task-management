from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

User = get_user_model()


class OnlyCustomer(BasePermission):
    message = _('Only customers are allowed to perform this action.')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.CUSTOMER


class OnlyEmployee(BasePermission):
    message = _('Only employees are allowed to perform this action.')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.EMPLOYEE
