import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        CUSTOMER = 'CUSTOMER', _('Customer')
        EMPLOYEE = 'EMPLOYEE', _('Employee')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("name of User"), max_length=255)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    phone = PhoneNumberField(null=True, blank=False)
    photo = models.ImageField(_("photo"), upload_to="users/")

    role = models.CharField(max_length=20, choices=Role)
    base_role = Role.ADMIN

    # only for customer (another way is to create profile for Customer)
    can_see_all_tasks = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class EmployeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYEE)


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Employee(User):
    base_role = User.Role.EMPLOYEE
    objects = EmployeeManager()

    class Meta:
        proxy = True


class Customer(User):
    base_role = User.Role.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True
