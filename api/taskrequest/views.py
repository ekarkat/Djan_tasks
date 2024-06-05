from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions import IsOwnerOrReadOnly
from taskmanager.models import TaskRequest
from .serializers import TaskRequestSerializer

from taskmanager import tasks

class TaskRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = TaskRequest.objects.all()
    serializer_class = TaskRequestSerializer

    @action(detail=False, methods=['get'], url_path='received_requests')
    def received_requests(self, request):
        # get current user recieved requests
        user = request.user
        addressed_tasks = TaskRequest.objects.filter(owner=user).all()
        serializer = TaskRequestSerializer(addressed_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sent_requests')
    def sent_requests(self, request):
        # get current user sent requests
        user = request.user
        sent_requests = TaskRequest.objects.filter(from_user=user).all()
        serializer = TaskRequestSerializer(sent_requests, many=True)
        return Response(serializer.data)
