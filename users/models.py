import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from . import managers


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        CUSTOMER = 'CUSTOMER', _('Customer')
        EMPLOYEE = 'EMPLOYEE', _('Employee')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("name of User"), max_length=255)
    email = models.EmailField(_("email address"))
    phone = PhoneNumberField(_("phone number"))
    photo = models.ImageField(_("photo"), upload_to="users")

    role = models.CharField(max_length=20, choices=Role)
    base_role = Role.ADMIN

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Employee(models.Model):
    base_role = User.Role.EMPLOYEE
    objects = managers.EmployeeManager()

    class Meta:
        proxy = True


class Customer(models.Model):
    base_role = User.Role.CUSTOMER
    objects = managers.CustomerManager()

    class Meta:
        proxy = True
