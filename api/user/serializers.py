from rest_framework import serializers
from administration.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']
