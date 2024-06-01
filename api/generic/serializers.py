from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.models import User
from taskmanager.models import Workspace, Unit, Task, TaskRequest


class TaskRequestSerializer(serializers.ModelSerializer):
    # user requests serializer with id, task, from_user, status fields
    # each request is connected to a task and user
    # each request has a status field to show the status of the request

    task = serializers.CharField(source='task.title', read_only=True)
    from_user = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = TaskRequest
        fields = ['id', 'task', 'from_user', 'owner', 'answer']

    def create(self, validated_data):
        # userrequest shouldnt be created from serializer
        return self

    def update(self, instance, validated_data):
        # update task request
        # set answer field
        instance.update(**validated_data)
        return instance

