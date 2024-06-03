from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

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

    @action(detail=False, methods=['get'], url_path='my_workspaces')
    def my_workspaces(self, request):
        # get current user workspaces
        user = request.user
        workspaces = Workspace.objects.filter(owner=user).all()
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)
