from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions import IsOwnerOrReadOnly
from taskmanager.models import TaskRequest
from .serializers import TaskRequestSerializer


class TaskRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = TaskRequest.objects.all()
    serializer_class = TaskRequestSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        # get current user recieved requests
        user = request.user
        addressed_tasks = TaskRequest.objects.filter(owner=user).all()
        serializer = TaskRequestSerializer(addressed_tasks, many=True)
        return Response(serializer.data)