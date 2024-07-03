from django.contrib.auth import get_user_model
from rest_framework import serializers

from tasks.models import Task
from .services import TaskService
from django.utils import timezone

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'customer': {'read_only': True},
            'report': {'read_only': True},
            'employee': {'read_only': True},
            'date_completed': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user = self.context['request'].user
        return TaskService.update_task(user, instance, validated_data)


class FinishTaskSerializer(serializers.Serializer):
    report = serializers.CharField(required=True)

    def validate(self, attrs):
        if not attrs.get('report'):
            raise serializers.ValidationError('Report field is required')
        return attrs

    def update(self, instance, validated_data):
        instance.report = validated_data.get('report')
        instance.date_completed = timezone.now()
        instance.status = Task.Status.DONE
        instance.save()
        return instance
