from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.task.serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from taskmanager.models import Task


class TaskViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
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
