from rest_framework import serializers

from taskmanager.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    # unit serializer with id, title, description, created_at, updated_at fields

    members = serializers.SerializerMethodField()
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Unit
        fields = ['id', 'owner', 'workspace', 'title', 'description', 'created_at', 'members', 'status']

    def get_members(self, obj):
        members = obj.members.all()
        members_output = []
        for member in members:
            members_output.append(member.username)
        return members_output
