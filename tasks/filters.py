from rest_framework import filters

from tasks.models import Task


class TaskStatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status')
        if status:
            status = status.lower()
            if status == 'pending':
                return queryset.filter(status=Task.Status.PENDING)
            elif status in ('running', 'in_progress'):
                return queryset.filter(status=Task.Status.RUNNING)
            elif status in ('finished', 'completed', 'done'):
                return queryset.filter(status.DONE)
        return queryset
