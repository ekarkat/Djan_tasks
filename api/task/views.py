from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from api.task.serializers import TaskSerializer
from taskmanager.models import Task


class TaskViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    # user profile view set with list, retrieve, create, update, destroy actions
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # lookup_field = 'user__username'
