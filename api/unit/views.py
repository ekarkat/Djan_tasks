from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from api.unit.serializers import UnitSerializer
from taskmanager.models import Unit


class UnitViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    # user profile view set with list, retrieve, create, update, destroy actions
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    # lookup_field = 'user__username'
