from rest_framework import serializers
from rest_framework.response import Response

from taskmanager.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    # unit serializer with id, title, description, created_at, updated_at fields

    members = serializers.SerializerMethodField()
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Unit
        fields = ['id', 'owner', 'workspace', 'title', 'description', 'created_at', 'members']

    def get_members(self, obj):
        members = obj.members.all()
        members_output = []
        for member in members:
            members_output.append(member.username)
        return members_output

    def __init__(self, *args, **kwargs):
        super(UnitSerializer, self).__init__(*args, **kwargs)

        # Check if 'request' is in the context and adjust the queryset for 'unit'
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['workspace'] = serializers.PrimaryKeyRelatedField(
                queryset=request.user.workspaces.all(),
                many=False
            )

    def validate(self, data):
        # Ensure the user can only create unit for their workspaces
        user = self.context['request'].user
        workspace = data.get('workspace')

        if not user.workspaces.filter(id=workspace.id).exists():
            raise serializers.ValidationError('You can only create units for your workspaces')
        return data

    def create(self, validated_data):
        # create unit
        # manually set owner field
        validated_data['owner'] = self.context['request'].user
        return Unit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('owner', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance






# class UnitCreateSerializer(serializers.Serializer):
#     # unit create serializer with title, description fields

#     title = serializers.CharField()
#     description = serializers.CharField()
#     workspace = serializers.CharField()

#     class Meta:
#         fields = (
#             'title',
#             'description',
#             'workspace',
#         )

#     def validate(self, data):
#         # Ensure the user can only create unit for their workspaces
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             raise serializers.ValidationError('You must be authenticated to create a unit')
#         workspace = data.get('workspace')
#         try:
#             workspace = int(workspace)
#         except:
#             raise serializers.ValidationError('Invalid workspace id')

#         user = self.context['request'].user
#         if not user.workspaces.filter(id=workspace).exists():
#             raise serializers.ValidationError('You can only create units for your workspaces')

#         return data

#     def create(self, validated_data):
#         validated_data['workspace'] = self.context['request'].user.workspaces.get(id=validated_data['workspace'])
#         unit = Unit.objects.create(**validated_data)
#         unit.save()

#         return unit

#     def to_representation(self, instance):
#         return UnitSerializer(instance).data


# class UnitUpdateSerializer(serializers.Serializer):
#     # unit update serializer with title, description fields

#     title = serializers.CharField(required=False)
#     description = serializers.CharField(required=False)
#     workspace = serializers.CharField(required=False)

#     class Meta:
#         fields = (
#             'title',
#             'description',
#             'workspace',
#         )

#     def validate(self, data):
#         # Ensure the user can only create unit for their workspaces
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             raise serializers.ValidationError('You must be authenticated to create a unit')
#         workspace = data.get('workspace')
#         try:
#             workspace = int(workspace)
#         except:
#             raise serializers.ValidationError('Invalid workspace id')

#         user = self.context['request'].user
#         if not user.workspaces.filter(id=workspace).exists():
#             raise serializers.ValidationError('You can only update units for your workspaces')

#         return data

#     def update(self, unit, validated_data):
#         validated_data.pop('owner', None)
#         validated_data['workspace'] = self.context['request'].user.workspaces.get(id=validated_data['workspace'])
#         for key, value in validated_data.items():
#             setattr(unit, key, value)
#         unit.save()

#         return unit

#     def to_representation(self, instance):
#         return UnitSerializer(instance).data
