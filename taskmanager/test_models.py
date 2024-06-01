from django.test import TestCase
from django.contrib.auth.models import User
from taskmanager.models import Workspace, Unit, Task, UnitComment, TaskComment, WorkSpaceComment, TaskRequest 

class WorkspaceModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workspace = Workspace.objects.create(
            title='Test Workspace',
            description='A test workspace',
            owner=self.user
            )
    
    def test_workspace_str(self):
        self.assertEqual(str(self.workspace), 'Test Workspace - testuser')
    
    
    def test_workspace_add_member(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.workspace.members.add(new_user)
        self.assertIn(new_user, self.workspace.members.all())

class UnitModelTest(TestCase):

    def setUp(self):
        """set up a database objects to test with"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workspace = Workspace.objects.create(
            title='Test Workspace',
            description='A test description',
            owner=self.user
        )
        self.unit= Unit.objects.create(
            title='Test Unit',
            owner=self.user,
            workspace = self.workspace
        )
    
    def test_unit_creation(self):
        self.assertEqual(self.unit.title, 'Test Unit')
        self.assertEqual(self.unit.owner, self.user)
        self.assertEqual(self.unit.workspace, self.workspace)
    
    def test_unit_str(self):
        self.assertEqual(str(self.unit), 'Test Unit - testuser')
    
class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workspace = Workspace.objects.create(
            title='Test Workspace',
            owner=self.user
        )
        self.unit = Unit.objects.create(
            title='Test Unit',
            owner=self.user,
            workspace=self.workspace
        )

    
    def test_task_status_choices(self):
        self.assertEqual(Task.StatusChoices.OPEN, 'OP')
        self.assertEqual(Task.StatusChoices.IN_PROGRESS, 'IN')
        self.assertEqual(Task.StatusChoices.CLOSED, 'CL')
        self.assertEqual(Task.StatusChoices.choices, [
            ('OP', 'Open'),
            ('IN', 'In Progress'),
            ('CL', 'Closed')
            ])

    def test_task_creation(self):
        task= Task.objects.create(
            title='Test Task',
            owner=self.user,
            unit=self.unit,
            workspace=self.workspace,
            status= Task.StatusChoices.OPEN,
            priority=Task.PriorityChoices.MEDIUM

        )
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.status, 'OP')
        self.assertEqual(task.priority, 'MD')
        self.assertEqual(str(task), 'Test Task - Test Unit')

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workspace = Workspace.objects.create(
            title='Test Workspace',
            owner=self.user
        )
        self.unit = Unit.objects.create(
            title='Test Unit',
            owner=self.user,
            workspace=self.workspace
        )
        self.task = Task.objects.create(
            title='Test Task',
            owner=self.user,
            unit=self.unit,
            workspace=self.workspace
        )

    def test_workspace_comment_creation(self):
        comment = WorkSpaceComment.objects.create(
            workspace=self.workspace,
            user=self.user,
            text='Test Workspace Comment'
        )
        self.assertEqual(comment.text, 'Test Workspace Comment')
        self.assertEqual(comment.workspace, self.workspace)
        self.assertEqual(comment.user, self.user)

    def test_unit_comment_creation(self):
        comment = UnitComment.objects.create(
            unit=self.unit,
            user=self.user,
            text='Test Unit Comment'
        )
        self.assertEqual(comment.text, 'Test Unit Comment')
        self.assertEqual(comment.unit, self.unit)
        self.assertEqual(comment.user, self.user)

    def test_task_comment_creation(self):
        comment = TaskComment.objects.create(
            task=self.task,
            user=self.user,
            text='Test Task Comment'
        )
        self.assertEqual(comment.text, 'Test Task Comment')
        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.user, self.user)