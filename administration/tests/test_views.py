"""Module for testing userprofile views"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from administration.models import UserProfile

class UserProfileViewsTest(TestCase):
    """TEST views class :  contains all the tests related to user profiles."""
    def setUp(self):
        """Set up a User and UserProfile objects
            make sure the database has the necessary data"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            email='testuser@exemple.com',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            image=None
        )
    
    def test_register_views_get(self):
        """Test the register view : Display the registration form"""
        response = self.client.get(reverse('administration:register')) # reverse ysed to get the URL fron the view name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration/register.htm')
    
    def test_register_views_post(self):
        """Test the Post request: process the form and registers a new
        new user"""
        response = self.client.post(reverse('administration:register'), {
            'username': 'newuser',
            'email': 'newuser@exemple.com',
            'password': 'password123',
            'confirm_password':'password123',
            'first_name': 'New',
            'last_name': 'User',
            'phone':'1234567890',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration/register_success.htm')
        self.assertTrue(User.objects.filter(username='newuser').exists())
