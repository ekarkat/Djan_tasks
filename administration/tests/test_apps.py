"""module to test the execution of the administration app"""

from django.test import TestCase
from django.apps import apps
from administration.apps import AdministrationConfig

class AdministrationConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AdministrationConfig.name, 'administration')
        self.assertEqual(apps.get_app_config('administration').name, 'administration')