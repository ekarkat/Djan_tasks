from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.task.serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from taskmanager.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    # user profile view set with list, retrieve, create, update, destroy actions
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    # serializer_class = TaskSerializer
    # lookup_field = 'user__username'

    def get_serializer_class(self):
        # get serializer class based on action
        if self.action == "create":
            return TaskCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
