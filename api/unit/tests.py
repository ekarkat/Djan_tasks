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

class UnitAPITest(APITestSetup):
    def setUp(self):
        super().setUp()
        self.workspace = Workspace.objects.create(title="Test Workspace", owner=self.user)
        
    def test_create_unit(self):
        data = {
            "title": "Test Unit",
            "description": "Test Description",
            "workspace": self.workspace.id
        }
        response = self.client.post(reverse('units-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Unit.objects.count(), 1)
        self.assertEqual(Unit.objects.get().title, "Test Unit")

    def test_retrieve_unit(self):
        unit = Unit.objects.create(title="Test Unit", owner=self.user, workspace=self.workspace)
        response = self.client.get(reverse('units-detail', kwargs={'pk': unit.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], unit.title)

    def test_update_unit(self):
        unit = Unit.objects.create(title="Test Unit", owner=self.user, workspace=self.workspace)
        data = {
            "title": "Updated Unit",
        }
        # response = self.client.patch(reverse('units-detail', kwargs={'pk': unit.pk}), data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # unit.refresh_from_db()
        # self.assertEqual(unit.title, "Updated Unit")

    def test_delete_unit(self):
        unit = Unit.objects.create(title="Test Unit", owner=self.user, workspace=self.workspace)
        response = self.client.delete(reverse('units-detail', kwargs={'pk': unit.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Unit.objects.count(), 0)