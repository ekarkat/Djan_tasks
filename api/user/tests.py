from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from administration.models import UserProfile
from django.urls import reverse

class APITestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(
            user=self.user,
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            phone='123456789',
            image=None
        )
        self.client.login(username='testuser', password='testpassword')

    def test_create_user_profile(self):
        self.client.logout()
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.login(username='newuser', password='newpassword')
        data = {
            "user": new_user.id,
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone": "987654321",
        }
        response = self.client.post(reverse('userprofile-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(UserProfile.objects.get(user=new_user).email, "newuser@example.com")

    def test_update_user_profile(self):
        data = {
            "first_name": "Updated",
            "last_name": "User"
        }
        response = self.client.patch(reverse('userprofile-detail', kwargs={'user__username': self.profile.user.username}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, "Updated")
        self.assertEqual(self.profile.last_name, "User")

    def test_delete_user_profile(self):
        response = self.client.delete(reverse('userprofile-detail', kwargs={'user__username': self.profile.user.username}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserProfile.objects.count(), 0)