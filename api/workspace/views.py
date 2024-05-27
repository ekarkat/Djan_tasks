from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from api.workspace.serializers import WorkspaceSerializer, WorkspaceCreateSerializer, WorkspaceUpdateSerializer
from taskmanager.models import Workspace


class WorkspaceViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    # workspace view set with list, retrieve, create, update, destroy actions
    permission_classes = [IsAuthenticated]
    queryset = Workspace.objects.all()
    # serializer_class = WorkspaceSerializer
    # lookup_field = 'title'

    def get_serializer_class(self):
        # get serializer class based on action
        if self.action == "create":
            return WorkspaceCreateSerializer
        if self.action in ['update', 'partial_update']:
            return WorkspaceUpdateSerializer
        return WorkspaceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
