from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskmanager.models import Unit
from .serializers import UnitSerializer, UnitCreateSerializer, UnitUpdateSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UnitCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UnitUpdateSerializer
        return UnitSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
