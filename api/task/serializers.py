from rest_framework import serializers
from rest_framework.response import Response

from taskmanager.models import Task, Unit, Workspace, TaskRequest


class TaskSerializer(serializers.ModelSerializer):
    # task serializer with id, title, description, created_at, updated_at, due_date, status fields
    owner = serializers.CharField(source='owner.username', read_only=True)
    workspace = serializers.IntegerField(source='workspace.id' ,read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'owner', 'addressed_to', 'workspace', 'unit', 'title', 'description', 'created_at', 'deadline', 'status', 'priority']

    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)
        # Check if 'request' is in the context and adjust the queryset for 'unit'
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['unit'] = serializers.PrimaryKeyRelatedField(
                queryset=Unit.objects.filter(owner=request.user),
                many=False
            )

    def validate(self, data):
        # Ensure the user can only create task for their units
        user = self.context['request'].user
        if not user.units.filter(id=data['unit'].id).exists():
            raise serializers.ValidationError('You can only create task for your units')
        return data

    def create(self, validated_data):
        # create task
        # manually set owner, workspace fields
        # set addressed_to field if exists

        addressed_to = validated_data.pop('addressed_to', None)
        validated_data['owner'] = self.context['request'].user
        validated_data['workspace'] = validated_data['unit'].workspace
        task = Task.objects.create(**validated_data)
        if addressed_to:
            task_request = TaskRequest.objects.create(task=task, owner=addressed_to, from_user=self.context['request'].user)
        return task

    def update(self, task, validated_data):
        # update task
        # set addressed_to field if exists
        addressed_to = validated_data.pop('addressed_to', None)
        for key, value in validated_data.items():
            setattr(task, key, value)
        task.save()
        if addressed_to:
            task_request = TaskRequest.objects.create(task=task, owner=addressed_to, from_user=self.context['request'].user)

        return task


# class TaskCreateSerializer(serializers.Serializer):
#     # task create serializer with title, description, due_date, status fields

#     title = serializers.CharField()
#     description = serializers.CharField()
#     status = serializers.ChoiceField(choices=Task.StatusChoices.choices)
#     priority = serializers.ChoiceField(choices=Task.PriorityChoices.choices)
#     deadline = serializers.DateField(required=False)
#     addressed_to = serializers.CharField(required=False)
#     unit = serializers.CharField()

#     class Meta:
#         fields = (
#             'title',
#             'description',
#             'status',
#             'priority',
#             'deadline',
#             'addressed_to',
#             'unit',
#         )

#     def validate(self, data):
#         # Ensure the user can only create task for their units

#         unit = data.get('unit')
#         try:
#             unit = int(unit)
#         except:
#             raise serializers.ValidationError('Invalid unit id')

#         if not user.units.filter(id=unit).exists():
#             raise serializers.ValidationError('You can only create task for your units')
#         return data

#     def create(self, validated_data):
#         # create task
#         # manually set owner, unit, workspace fields
#         # set addressed_to field if exists

#         validated_data.pop('addressed_to', None) # remove addressed_to field if exists
#         validated_data['owner'] = self.context['request'].user
#         validated_data['unit'] = self.context['request'].user.units.get(id=validated_data['unit'])
#         validated_data['workspace'] = validated_data['unit'].workspace
#         task = Task.objects.create(**validated_data)

#         return task

#     def to_representation(self, instance):
#         return TaskSerializer(instance).data
#         # return Response({'test':'working'}).data


# class TaskUpdateSerializer(serializers.Serializer):
#     # task update serializer with title, description, due_date, status fields

#     title = serializers.CharField(required=False)
#     description = serializers.CharField(required=False)
#     status = serializers.ChoiceField(choices=Task.StatusChoices.choices, required=False)
#     priority = serializers.ChoiceField(choices=Task.PriorityChoices.choices, required=False)
#     deadline = serializers.DateField(required=False)
#     addressed_to = serializers.CharField(required=False)
#     # unit = serializers.IntegerField(source='unit.id', required=False)

#     class Meta:
#         fields = (
#             'title',
#             'description',
#             'status',
#             'priority',
#             'deadline',
#             'addressed_to',
#             'unit',
#         )

#     # def validate(self, data):
#     #     # Ensure the user can only update a task for their units
#     #     unit = data.get('unit')
#     #     try:
#     #         unit = int(unit['id'])
#     #     except:
#     #         raise serializers.ValidationError('Invalid unit id')

#     #     if not user.units.filter(id=unit).exists():
#     #         raise serializers.ValidationError('You can only update task for your units')

#     #     return data

#     def update(self, task, validated_data):
#         # update task
#         # set addressed_to field if exists
#         # set owner, unit, workspace fields
#         validated_data.pop('addressed_to', None) # to be build later 
#         # validated_data['unit'] = self.context['request'].user.units.filter(id=validated_data['unit']['id']).first()
#         validated_data['unit'] = self.context['request'].user.units.filter(id=validated_data['unit']['id']).first()
#         for key, value in validated_data.items():
#             setattr(task, key, value)
#         task.save()

#         return task

#     def to_representation(self, instance):
#         return TaskSerializer(instance).data
