from django.test import TestCase
from django.contrib.auth.models import User
from administration.forms import RegisterForm, LoginForm

class RegisterFromTest(TestCase):
    """Test the administration app form"""
    def test_register_form_valid_data(self):
        """Valid data form test"""
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@exemple.com',
            'password': '1234567890',
            'confirm_password': '1234567890',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '0987654321',
        })
        self.assertTrue(form.is_valid())
    

    def test_register_form_invalid_data(self):
        """Invalid case tesr"""
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7) # 7 fields are required

class LoginFormTest(TestCase):
    def test_login_form_valid_data(self):
        user = User.objects.create_user(username='testuser', password='1234567890')
        form = LoginForm(data={
            'username':'testuser',
            'password':'1234567890'
        })

        self.assertTrue(form.is_valid())
    

    def test_login_form_invalid_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)