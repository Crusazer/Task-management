from django.contrib.auth import get_user_model
from rest_framework import filters

from tasks.models import Task

User = get_user_model()


class UserRoleFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        role = request.query_params.get('role')
        if role:
            role = role.lower()
            if role == 'employee':
                return queryset.filter(role=User.Role.EMPLOYEE)
            elif role == 'customer':
                return queryset.filter(role=User.Role.CUSTOMER)
            return queryset.none()

        return queryset
