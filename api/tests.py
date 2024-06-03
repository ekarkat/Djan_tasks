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
    

# class AuthenticationTest(APITestSetup):
#     def test_authentication_required(self):
#         self.client.logout()
#         response = self.client.get(reverse('user-list'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
#         response = self.client.get(reverse('workspace-list'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
#         response = self.client.get(reverse('units-list'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
#         response = self.client.get(reverse('tasks-list'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)