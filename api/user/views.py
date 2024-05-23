from rest_framework.response import Response
from rest_framework.decorators import api_view
from administration.models import UserProfile
from api.user.serializers import UserProfileSerializer

@api_view(['GET'])
def user_list(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)
