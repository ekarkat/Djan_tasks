from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from api.workspace.serializers import WorkspaceSerializer
from taskmanager.models import Workspace


class WorkspaceViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    # workspace view set with list, retrieve, create, update, destroy actions
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    # lookup_field = 'title'


