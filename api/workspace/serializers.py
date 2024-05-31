from rest_framework import serializers

from taskmanager.models import Workspace, Unit


class UnitSerializer(serializers.ModelSerializer):
    # unit serializer with id, title, description, created_at, updated_at, workspace fields
    # workspace = serializers.CharField(source='workspace.title', read_only=True)
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

# class WorkspaceCreateSerializer(serializers.Serializer):
#     # workspace create serializer with title, description fields

#     title = serializers.CharField()
#     description = serializers.CharField()

#     class Meta:
#         fields = (
#             'title',
#             'description',
#         )

#     def validate(self, data):
#         # Ensure the is a  registered user
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             raise serializers.ValidationError('You must be authenticated to create a workspace')
#         return data

#     def create(self, validated_data):
#         print(validated_data)
#         workspace = Workspace.objects.create(**validated_data)

#         return workspace

#     def to_representation(self, instance):
#         return WorkspaceSerializer(instance).data


# class WorkspaceUpdateSerializer(serializers.Serializer):
#     # workspace update serializer with title, description fields

#     title = serializers.CharField()
#     description = serializers.CharField()

#     class Meta:
#         fields = (
#             'title',
#             'description',
#         )

#     def update(self, workspace, validated_data):
#         workspace.title = validated_data.get('title', workspace.title)
#         workspace.description = validated_data.get('description', workspace.description)
#         workspace.save()

#         return workspace

#     def to_representation(self, instance):
#         return WorkspaceSerializer(instance).data
