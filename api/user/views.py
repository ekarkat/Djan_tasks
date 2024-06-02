from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from administration.models import UserProfile
from api.user.serializers import UserProfileSerializer, UserProfileCreateSerializer, UserProfileUpdateSerializer
from api.generic.serializers import TaskRequestSerializer
from taskmanager.models import TaskRequest

class UserProfileViewSet(viewsets.ModelViewSet):
    # user profile view set with list, retrieve, create, update, destroy actions
    queryset = UserProfile.objects.all()
    # serializer_class = UserProfileSerializer # remove after using get_serializer_class
    lookup_field = 'user__username'

    def get_serializer_class(self):
        # get serializer class based on action
        if self.action == "create":
            return UserProfileCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        # get current user profile
        user = request.user
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

