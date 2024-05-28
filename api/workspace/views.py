from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.workspace.serializers import WorkspaceSerializer
from taskmanager.models import Workspace
from api.permissions import IsOwnerOrReadOnly


class WorkspaceViewSet(viewsets.ModelViewSet):
    # workspace view set with list, retrieve, create, update, destroy actions
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    # lookup_field = 'title'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context
