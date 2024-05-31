from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User

from taskmanager.models import Workspace, Unit, Task, TaskRequest


class UserRequestsSerializer(serializers.ModelSerializer):
    # user requests serializer with id, task, from_user, status fields
    # each request is connected to a task and user
    # each request has a status field to show the status of the request

    task = serializers.CharField(source='task.title', read_only=True)
    from_user = serializers.CharField(read_only=True)

    class Meta:
        model = TaskRequest
        fields = ['id', 'task', 'from_user', 'answer']


    def update(self, instance, validated_data):
        # update task request
        # set answer field
        instance.update(**validated_data)
        return instance