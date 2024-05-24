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
