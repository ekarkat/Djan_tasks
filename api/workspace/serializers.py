from rest_framework import serializers

from taskmanager.models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    # workspace serializer with id, title, description, created_at, updated_at fields

    owner = serializers.CharField(source='owner.username')
    members = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'owner', 'title', 'description', 'created_at', 'updated_at', 'members', 'units']

    def get_members(self, obj):
        members = obj.members.all()
        members_output = []
        for member in members:
            members_output.append(member.username)
        return members_output

    def get_units(self, obj):
        units = obj.units.all()
        unit_output = []
        for unit in units:
            unit_details = {
                'id': unit.id,
                'title': unit.title,
            }
            unit_output.append(unit_details)
        return unit_output


class WorkspaceCreateSerializer(serializers.Serializer):
    # workspace create serializer with title, description fields

    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        fields = (
            'title',
            'description',
        )

    def validate(self, data):
        # Ensure the is a  registered user
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError('You must be authenticated to create a workspace')
        return data

    def create(self, validated_data):
        print(validated_data)
        workspace = Workspace.objects.create(**validated_data)

        return workspace

    def to_representation(self, instance):
        return WorkspaceSerializer(instance).data


class WorkspaceUpdateSerializer(serializers.Serializer):
    # workspace update serializer with title, description fields

    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        fields = (
            'title',
            'description',
        )

    def update(self, workspace, validated_data):
        workspace.title = validated_data.get('title', workspace.title)
        workspace.description = validated_data.get('description', workspace.description)
        workspace.save()

        return workspace

    def to_representation(self, instance):
        return WorkspaceSerializer(instance).data
