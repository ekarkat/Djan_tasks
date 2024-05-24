from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User

from administration.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # user profile serializer with id, email, first_name, last_name, phone fields

    username = serializers.CharField(source='user.username')
    workspace = serializers.SerializerMethodField()
    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserProfile
        fields = ['id', 'created_at', 'username','email', 'first_name', 'last_name', 'phone', 'workspace']

    def get_workspace(self, obj):
        # Optimized fetching should be handled in the viewset
        return [{'id': ws.id, 'title': ws.title} for ws in obj.user.workspaces.all()]


class UserProfileCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        # model = UserProfile
        fields = (
            'username',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'phone',
        )

    def validate(self, attrs):
        if User.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError('username already exist')

        if UserProfile.objects.filter(email=attrs.get('email')).exists():
            raise ValidationError('email already exist')

        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError("passwords don't match")

        return attrs

    def create(self, validated_data):
        #  do it yourself!!!!
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        _ = validated_data.pop('confirm_password')
        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user
        instance = UserProfile.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        return UserProfileSerializer(instance).data
