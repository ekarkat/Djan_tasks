import json

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel

# Create your models here.
# user.workspace = workspace.object.filter(owner = user).all()
# 
class Workspace(BaseModel):
    # workspace class with title, description, owner, members fields
    # each workspace has a title, description, owner, members
    # each workspace has tasks that can be accessed by workspace.task_set.all()
    # each workspace has comments that can be accessed by workspace.comments.all()
    # A user can access the workspaces they own by user.workspaces.all()
    # A user can access the workspaces they are members of by user.shared_workspaces.all()

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    members = models.ManyToManyField(User, related_name='shared_workspaces', blank=True)
    status = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title + ' - ' + self.owner.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            instance = super(Workspace, self).save()
            text = f"Created by {self.owner.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            instance = super(Workspace, self).save()
            text = f"Updated by {self.owner.username} at {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"

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
    # A user can access their units by user.units.all()
    # A user can access the units shared with them by user.shared_units.all()

    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='units')
    members = models.ManyToManyField(User, related_name='shared_units', blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='units')
    status = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['created_at']

    def __str__(self):
        return (self.title + ' - '  + self.workspace.title + ' - ' + self.owner.username)

    def save(self, *args, **kwargs):
        if self.pk is None:
            instance = super(Unit, self).save()
            text = f"Created by {self.owner.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            instance = super(Unit, self).save()
            text = f"Updates by {self.owner.username} at {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"

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
        EXPIRED = 'EX', 'Expired'

    class PriorityChoices(models.TextChoices):
        LOW = 'LW', 'Low'
        MEDIUM = 'MD', 'Medium'
        HIGH = 'HG', 'High'

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    addressed_to = models.ForeignKey(User, related_name='addressed_tasks', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tasks')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        out = self.title + ' - ' + self.unit.title
        return out

    def save(self, *args, **kwargs):
        if self.pk is None:
            instance = super(Task, self).save()
            text = f"Created by {self.owner.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            if self.deadline:
                PeriodicTask.objects.create(
                        crontab= CrontabSchedule.objects.create(
                        minute = self.deadline.minute,
                        hour = self.deadline.hour,
                        day_of_month = self.deadline.day,
                        month_of_year = self.deadline.month,
                    ),
                    name = f'{self.id}',
                    task = 'taskmanager.tasks.check_deadline',
                    kwargs = json.dumps({'task_id': self.id}),
                    enabled = True,
                    one_off = True
                )
        else:
            instance = super(Task, self).save()
            text = f"Updated by {self.owner.username} at {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
            if self.deadline:
                try:
                    periodic_task = PeriodicTask.objects.get(name=f'{self.id}')
                    periodic_task.crontab, created = CrontabSchedule.objects.get_or_create(
                        minute = self.deadline.minute,
                        hour = self.deadline.hour,
                        day_of_month = self.deadline.day,
                        month_of_year = self.deadline.month,
                    )
                    periodic_task.enabled = True
                    periodic_task.one_off = True
                    periodic_task.save()
                except PeriodicTask.DoesNotExist:
                    PeriodicTask.objects.create(
                        crontab, created = CrontabSchedule.objects.get_or_create(
                            minute = self.deadline.minute,
                            hour = self.deadline.hour,
                            day_of_month = self.deadline.day,
                            month_of_year = self.deadline.month,
                        ),
                        name = f'{self.id}',
                        task = 'taskmanager.tasks.check_deadline',
                        kwargs = json.dumps({'task_id': self.id}),
                        enabled = True,
                        one_off=True
                    )

        TaskComment.objects.create(task=self, user=self.owner, text=text)

        return instance

    def address_this_task(self, user):
        # address a task to a user
        if User.objects.filter(id=user.id).exists():
            task_request = TaskRequest.objects.create(task=slef, owner=user, from_user=self.owner)
            return task_request
        return None


class WorkSpaceComment(BaseModel):
    # comment class with workspace and user fields
    # each comment is connected to a workspace and user
    # each comment has a text field for the comment content

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='comments')
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


class TaskRequest(BaseModel):
    # task request class with task, user, and status fields
    # each task request is connected to a task and user
    # each task request has a status field to show the status of the request
    # a user can access their requests by user.sent_requests.all()

    class AnswerChoices(models.TextChoices):
        PENDING = 'PD', 'Pending'
        ACCEPTED = 'AC', 'Accepted'
        REJECTED = 'RJ', 'Rejected'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='requests')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests') # owner = addressed_to
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    answer = models.CharField(max_length=20, choices=AnswerChoices.choices, default=AnswerChoices.PENDING)

    def __str__(self):
        out = self.task.title + ' - ' + self.owner.username
        return out

    def update(self, *args, **kwargs):
        # address a task to a user in case answer is 'AC'

        if self.answer == TaskRequest.AnswerChoices.ACCEPTED:
            # if the answer for the task is already = Accepted, dont do anything
            return self
        else:
            if kwargs.get('answer') == 'AC':
                self.task.addressed_to = self.owner
                self.task.save()
                self.answer = TaskRequest.AnswerChoices.ACCEPTED
                super(TaskRequest, self).save()
            else:
                self.answer = kwargs.get('answer')
                super(TaskRequest, self).save()
