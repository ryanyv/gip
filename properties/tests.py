from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property


class AddPropertyPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.admin = User.objects.create_user(
            username="admin", password="pass", role="admin"
        )

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("add_property"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_regular_user_redirected(self):
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse("add_property"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_admin_can_access(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("add_property"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_property(self):
        self.client.login(username="admin", password="pass")
        data = {
            "name": "Test Property",
            "property_type": "short-term",
            "location": "Test City",
            "description": "Nice place",
            "guests": 2,
            "bedrooms": 1,
            "bathrooms": 1,
        }
        response = self.client.post(reverse("add_property"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Property.objects.filter(name="Test Property").exists())

