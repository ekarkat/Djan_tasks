"""Module to test administration app urls are correctly mapped to the
    corresponding view functions. TO ensure that when a URL is accessed
    the expected view is called
"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve # resolves a URL path to the corresponding view function
from administration.views import register, user_login, custom_logout

class TestUrls(SimpleTestCase):
    """The use of simpleTestCase class: it is a django class that doesn't use
        the database, suitable for the lightweight test like URL resolution
    """
    def test_register_url_resolves(self):
        url = reverse('administration:register')
        self.assertEqual(resolve(url).func, register)
        # resolve(url): resolves the URL path to the view function that handles this url
        # .func: extract the view function from the resolved URL
    
    def test_login_url_resolves(self):
        url = reverse('administration:login')
        self.assertEqual(resolve(url).func, user_login)
    
    def test_logout_url_resolves(self):
        url = reverse('administration:logout')
        self.assertEqual(resolve(url).func, custom_logout)