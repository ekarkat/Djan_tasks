from rest_framework import serializers

from taskmanager.models import Task


class TaskSerializer(serializers.ModelSerializer):
    # task serializer with id, title, description, created_at, updated_at, due_date, status fields

    owner = serializers.CharField(source='owner.username')
    addressed_to = serializers.SerializerMethodField()
    unit = serializers.CharField(source='unit.id')
    workspace = serializers.CharField(source='workspace.id')

    class Meta:
        model = Task
        fields = ['id', 'owner', 'addressed_to', 'unit', 'workspace', 'title', 'description', 'created_at', 'deadline', 'status', 'priority']

    def get_addressed_to(self, obj):
        if obj.addressed_to:
            return obj.addressed_to.username
        return None
