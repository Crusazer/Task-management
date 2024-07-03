from django.urls import path

from tasks.views import (
    CreateTaskView,
    TaskListRetrieveView,
    TakeTaskView,
    UpdateTaskView,
    FinishTaskView
)

urlpatterns = [
    path('', TaskListRetrieveView.as_view(), name='task-list'),
    path('<int:pk>/', TaskListRetrieveView.as_view(), name='task-detail'),
    path('create/', CreateTaskView.as_view(), name='task-create'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='task-update'),
    path('take/<int:pk>/', TakeTaskView.as_view(), name='task-take'),
    path('finish/<int:pk>/', FinishTaskView.as_view(), name='task-finish'),
]
