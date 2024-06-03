from django.test import TestCase
from django.contrib.auth.models import User
from administration.models import UserProfile

class UserProfileModelTest(TestCase):
    """test the userProfileModel class"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            phone='1234567890',
            image=None
        )

    def test_user_profile_creation(self):
        '''creation of a user'''
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.email, 'testuser@example.com')
        self.assertEqual(self.user_profile.first_name, 'Test')
        self.assertEqual(self.user_profile.last_name, 'User')
        self.assertEqual(self.user_profile.phone,'1234567890')
    


    def test_user_profile_str_method(self):
        """string format"""
        self.assertEqual(str(self.user_profile), f'id :{self.user_profile.id} - testuser')