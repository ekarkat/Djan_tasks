from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsOwnerOrReadOnly
from taskmanager.models import TaskRequest
from .serializers import UserRequestsSerializer


class UserRequestsViewSet(viewsets.ModelViewSet):
    queryset = TaskRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserRequestsSerializer

