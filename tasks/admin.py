from django.contrib import admin

from tasks.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status')
    list_filter = ('status',)
    search_fields = ('id', 'title')
    fields = ('id',
              'title',
              'status',
              'description',
              'report',
              'date_created',
              'date_updated',
              'date_completed',
              'customer',
              'employee')
    readonly_fields = ('id', 'date_created', 'date_updated', 'date_completed')
