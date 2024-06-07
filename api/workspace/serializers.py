from rest_framework import serializers

from taskmanager.models import Workspace, Unit


class UnitSerializer(serializers.ModelSerializer):
    # unit serializer with id, title
    class Meta:
        model = Unit
        fields = ['id', 'title']


class WorkspaceSerializer(serializers.ModelSerializer):
    # workspace serializer with id, title, description, created_at, updated_at fields

    owner = serializers.CharField(source='owner.username', read_only=True)
    members = serializers.SerializerMethodField()
    units = UnitSerializer(many=True, read_only=True)  # Handle multiple units

    class Meta:
        model = Workspace
        fields = ['id', 'owner', 'title', 'description', 'created_at', 'updated_at', 'members', 'units']

    def get_members(self, obj):
        members = obj.members.all()
        members_output = []
        for member in members:
            members_output.append(member.username)
        return members_output

    def create(self, validated_data):
        # create workspace
        # manually set owner field
        validated_data['owner'] = self.context['request'].user
        return Workspace.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('owner', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
