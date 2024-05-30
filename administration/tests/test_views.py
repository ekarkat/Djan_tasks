"""Module for testing userprofile views"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from administration.models import UserProfile
from django.contrib.auth import get_user_model

class UserProfileViewsTest(TestCase):
    """TEST views class :  contains all the tests related to user profiles."""
    def setUp(self):
        """Set up a User and UserProfile objects
            make sure the database has the necessary data"""
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
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

    
    def test_login_views_get(self):
        """Test the get request to login view : Display the login form"""
        response = self.client.get(reverse('administration:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration/login.html')
    
    def test_login_view_post_valid(self):
        """Test the valid post request"""
        response= self.client.post(reverse('administration:login'), {
            'username': 'testuser',
            'password':'testpassword'
        })
        self.assertRedirects(response, reverse('core:home'))
    
    def test_login_view_post_invalid_username(self):
        """Test the invalid post request for the login view"""
        response = self.client.post(reverse('administration:login'), {
            'username': 'wronguser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration/login.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    

    def test_login_view_post_invalid_password(self):
        """Test the invalid post request for the login view"""
        response = self.client.post(reverse('administration:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration/login.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_login_view_post_blank_fields(self):
        response = self.client.post(reverse('administration:login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administration/login.html')
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_login_view_authenticated_user(self):
        """Test user authentication"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('administration:login'))
        self.assertRedirects(response, reverse('core:home'))
    