from rest_framework.permissions import BasePermission, SAFE_METHODS
from administration.models import UserProfile

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an 'owner' attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner or addressed to.
        if hasattr(obj, 'addressed_to'):
            return (obj.owner == request.user) or (obj.addressed_to == request.user)
        if (isinstance(obj, UserProfile)):
            return obj.user == request.user
        return obj.owner == request.user
