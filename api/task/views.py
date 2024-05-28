from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.task.serializers import TaskSerializer
from taskmanager.models import Task
from api.permissions import IsOwnerOrReadOnly

class TaskViewSet(viewsets.ModelViewSet):
    # user profile view set with list, retrieve, create, update, destroy actions
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     return Task.objects.filter(owner=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context
