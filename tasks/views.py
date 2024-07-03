from django.db.models import Q
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from tasks.models import Task
from .filters import TaskStatusFilter
from .services import TaskService
from .permissions import OnlyCustomer, OnlyEmployee
from .serializers import (
    TaskSerializer,
    FinishTaskSerializer,
)


# Create your views here.
class CreateTaskView(generics.CreateAPIView):
    """ Only Customer can create task """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [OnlyCustomer]


class TaskListRetrieveView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    """ Show tasks for a user based on their permissions. """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [TaskStatusFilter]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return TaskService.get_queryset_tasks_for_user(self.request.user)


class TakeTaskView(generics.GenericAPIView):
    queryset = Task.objects.all()
    permission_classes = [OnlyEmployee]

    def post(self, request, *args, **kwargs):
        if TaskService.set_employer_for_task(self.request, kwargs['pk']):
            return Response({'detail': 'Task has been taken successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'You are not allowed to take this task or it is already assigned.'},
                        status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskView(generics.UpdateAPIView):
    """
    If task pending customer can change title and description.
    Employee can change report if task status is running.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class FinishTaskView(generics.GenericAPIView):
    """    Only Employee of the task can finish it.    """
    serializer_class = FinishTaskSerializer
    permission_classes = [OnlyEmployee]

    def post(self, request, *args, **kwargs):
        if TaskService.finish_task(request, kwargs['pk'], self.serializer_class):
            return Response({'detail': 'Task has been finished successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'You are not allowed to take this task or it is already assigned.'},
                        status=status.HTTP_400_BAD_REQUEST)
