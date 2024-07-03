from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskService:
    @staticmethod
    def get_queryset_tasks_for_user(user):
        """
          Customer can see own tasks or all tasks if he has permission to see all tasks.
          Employer can see all pending tasks and tasks he has performed or completed.
        """
        if user.role == User.Role.CUSTOMER:
            if user.can_see_all_tasks:
                return Task.objects.all()
            else:
                return Task.objects.filter(customer=user)

        if user.role == User.Role.EMPLOYEE:
            return Task.objects.filter(Q(status=Task.Status.PENDING) | Q(employee=user))

        if user.role == User.Role.ADMIN:
            return Task.objects.all()

        return Task.objects.none()

    @staticmethod
    def set_employer_for_task(request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.status == Task.Status.PENDING:
            task.status = Task.Status.RUNNING
            task.employee = request.user
            task.save()
            return True
        return False

    @staticmethod
    def update_task(user, instance, validated_data):
        if instance.customer == user and instance.status == Task.Status.PENDING:
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance

        if instance.employee == user and instance.status == Task.Status.RUNNING:
            instance.report = validated_data.get('report', instance.report)
            instance.save()
            return instance
        raise PermissionDenied('You do not have permission to update this task.')

    @staticmethod
    def finish_task(request, pk, serializer_class):
        task = get_object_or_404(Task, pk=pk)
        if request.user == task.employee and task.status == Task.Status.RUNNING:
            serializer = serializer_class(instance=task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(status=Task.Status.DONE)
            return True
        return False
