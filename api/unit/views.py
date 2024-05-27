from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from api.unit.serializers import UnitSerializer, UnitCreateSerializer, UnitUpdateSerializer
from taskmanager.models import Unit


class UnitViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    # user profile view set with list, retrieve, create, update, destroy actions
    permission_classes = [IsAuthenticated]
    queryset = Unit.objects.all()
    # serializer_class = UnitSerializer
    # lookup_field = 'user__username'

    def get_serializer_class(self):
        # get serializer class based on action
        if self.action == "create":
            return UnitCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UnitUpdateSerializer
        return UnitSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
