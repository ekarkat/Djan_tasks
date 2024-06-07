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
        # workspace field representation
        return [{'id': ws.id, 'title': ws.title} for ws in obj.user.workspaces.all()]


class UserProfileCreateSerializer(serializers.Serializer):
    # user profile create serializer with

    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    image = serializers.ImageField(required=False)

    class Meta:
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'phone',
            'image',
            ]

    def validate(self, data):
        # Ensure the new email, username is not already in use by another user

        if User.objects.filter(username=data.get('username')).exists():
            raise ValidationError('username already exist')

        if UserProfile.objects.filter(email=data.get('email')).exists():
            raise ValidationError('email already exist')

        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("passwords don't match")

        return data

    def create(self, validated_data):
        # Create a new user and user profile
        # print(validated_data)
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        _ = validated_data.pop('confirm_password')
        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user
        instance = UserProfile.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        # return the user profile data
        return UserProfileSerializer(instance).data


class UserProfileUpdateSerializer(serializers.Serializer):
    # user profile update serializer

    username = serializers.CharField(source='user.username')
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    image = serializers.ImageField(required=False)

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'image']

    def validate(self, data):
        # Ensure the new email, username is not already in use by another user
        username = data.get('user').get('username')
        if not username:
            raise ValidationError('user is required')
        if User.objects.filter(username=username).exclude(username=self.instance.user.username).exists():
            raise ValidationError('username already exist')
        if UserProfile.objects.filter(email=data.get('email')).exclude(user=self.instance.user).exists():
            raise ValidationError('email already exist')
        return data

    def update(self, userprofile, validated_data):
        # Update the User and UserProfile from validated_data

        user_data = validated_data.pop('user', {})
        userprofile.user.username = user_data.get('username', userprofile.user.username)
        userprofile.user.save()

        for attr, value in validated_data.items():
            setattr(userprofile, attr, value)
        userprofile.save()

        return userprofile
