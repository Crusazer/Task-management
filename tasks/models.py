from django.db import models

from users.models import Customer, Employee
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', _('Pending')
        IN_PROGRESS = 'I', _('In Progress')
        DONE = 'D', _('Done')

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    report = models.TextField(blank=True, null=True, verbose_name=_('Report'))
    status = models.CharField(max_length=1, choices=Status, default=Status.PENDING,
                              db_index=True, verbose_name=_('Status'))

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date updated'))
    date_completed = models.DateTimeField(blank=True, null=True, verbose_name=_('Date completed'))

    customer = models.ForeignKey(Customer,
                                 null=True,
                                 blank=False,
                                 on_delete=models.SET_NULL,
                                 related_name='created_tasks',
                                 verbose_name=_('Customer'))
    employee = models.ForeignKey(Employee,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='tasks',
                                 verbose_name=_('Employee'))

    def save(self, *args, **kwargs):
        if self.status == Task.Status.DONE and not self.report:
            raise ValueError('Report must be provided for completed tasks.')
        if self.status == Task.Status.DONE and not self.date_completed:
            raise ValueError('Date completed must be provided for completed tasks.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
