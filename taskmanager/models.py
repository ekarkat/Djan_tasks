from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel

# Create your models here.

class WorkSpace(BaseModel):
    # workspace class with title, description, owner, members fields
    # each workspace has a title, description, owner, members
    # each workspace has tasks that can be accessed by workspace.task_set.all()
    # each workspace has comments that can be accessed by workspace.comments.all()
    # A user can access the workspaces they own by user.workspaces.all()
    # A user can access the workspaces they are members of by user.member_workspaces.all()

    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    members = models.ManyToManyField(User, related_name='member_workspaces')
    status = models.FloatField()

    def __str__(self):
        return self.title + ' - ' + self.owner.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            text = f'Created by {self.owner.username} at {self.created_at}'
            instance = super(WorkSpace, self).save()
        else:
            text = f'Updated by {self.owner.username} at {self.updated_at}'
            instance = super(WorkSpace, self).save()

        WorkSpaceComment.objects.create(workspace=self, user=self.owner, text=text)

        return instance

    class Meta:
        verbose_name = 'WorkSpace'
        verbose_name_plural = 'WorkSpaces'
        ordering = ['created_at']


class Unit(BaseModel):
    # unit class with status and priority choices
    # each unit contains multiple tasks that can be acceced by unit.tasks.all()
    # each unit has owner that can be accessed by unit.owner
    # each unit has members that can be accessed by unit.members.all()
    # A user can access their todo list by user.units.all()
    # A user can access the todo lists shared with them by user.shared_units.all()

    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='units')
    members = models.ManyToManyField(User, related_name='shared_units')
    status = models.FloatField()
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name='units')

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['created_at']

    def __str__(self):
        return (self.title + ' - ' + self.owner.username)

    def save(self, *args, **kwargs):
        if self.pk is None:
            text = f'Created by {self.owner.username} at {self.created_at}'
            instance = super(Unit, self).save()
        else:
            text = f'Updated by {self.owner.username} at {self.updated_at}'
            instance = super(Unit, self).save()

        UnitComment.objects.create(unit=self, user=self.owner, text=text)

        return instance


class Task(BaseModel):
    # task class with status and priority choices
    # each task has a todo that can be accessed by task.unit
    # each task has a creator that can be accessed by task.created_by
    # each task can be accessed to users,  task.addressed_to.all()
    # A user can access the tasks they created by user.created_tasks.all()
    # A user can access the tasks they are assigned to by user.addressed_tasks.all()

    class StatusChoices(models.TextChoices):
        OPEN = 'OP', 'Open'
        IN_PROGRESS = 'IN', 'In Progress'
        CLOSED = 'CL', 'Closed'

    class PriorityChoices(models.TextChoices):
        LOW = 'LW', 'Low'
        MEDIUM = 'MD', 'Medium'
        HIGH = 'HG', 'High'

    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    addressed_to = models.ManyToManyField(User, related_name='addressed_tasks')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tasks')
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        out = self.title + ' - ' + self.unit.title
        return out

    def save(self):
        if self.pk is None:
            TaskComment.objects.create(todo=instance, user=request.user, text=f'Created by {self.owner.username}')


class WorkSpaceComment(BaseModel):
    # comment class with workspace and user fields
    # each comment is connected to a workspace and user
    # each comment has a text field for the comment content

    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        out = self.text + ' - ' + self.workspace.title
        return out


class UnitComment(BaseModel):
    # comment class with todo and user fields
    # each comment is connected to a todo and user
    # each comment has a text field for the comment content

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        out = self.text + ' - ' + self.unit.title
        return out


class TaskComment(BaseModel):
    # comment class with task and user fields
    # each comment is connected to a task and user
    # each comment has a text field for the comment content

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        out = self.text + ' - ' + self.task.title
        return out
