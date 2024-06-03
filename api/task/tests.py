from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from taskmanager.models import Unit, Workspace, Task
from administration.models import UserProfile
from django.urls import reverse

class APITestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

class TaskAPITest(APITestSetup):
    def setUp(self):
        super().setUp()
        self.workspace = Workspace.objects.create(title="Test Workspace", owner=self.user)
        self.unit = Unit.objects.create(title="Test Unit", owner=self.user, workspace=self.workspace)

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "unit": self.unit.id,
            "workspace": self.workspace.id,
            "status": "OP",
            "priority": "MD"
        }
        # response = self.client.post(reverse('tasks-list'), data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Task.objects.count(), 1)
        # self.assertEqual(Task.objects.get().title, "Test Task")

    def test_retrieve_task(self):
        task = Task.objects.create(title="Test Task", owner=self.user, unit=self.unit, workspace=self.workspace)
        response = self.client.get(reverse('tasks-detail', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_update_task(self):
        task = Task.objects.create(title="Test Task", owner=self.user, unit=self.unit, workspace=self.workspace)
        data = {
            "title": "Updated Task",
        }
        # response = self.client.patch(reverse('tasks-detail', kwargs={'pk': task.pk}), data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # task.refresh_from_db()
        # self.assertEqual(task.title, "Updated Task")

    def test_delete_task(self):
        task = Task.objects.create(title="Test Task", owner=self.user, unit=self.unit, workspace=self.workspace)
        response = self.client.delete(reverse('tasks-detail', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)