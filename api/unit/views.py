from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from taskmanager.models import Unit
from .serializers import UnitSerializer
from api.permissions import IsOwnerOrReadOnly

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UnitSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context

    @action(detail=False, methods=['get'], url_path='my_units')
    def my_units(self, request):
        user = request.user
        units = Unit.objects.filter(owner=user).all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)
