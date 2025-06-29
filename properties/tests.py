from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import Property, Booking
from django.core.files.uploadedfile import SimpleUploadedFile
from urllib.parse import urlencode


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
        prop = Property.objects.get(name="Test Property")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.responsible, self.admin)

    def test_admin_can_upload_photos(self):
        self.client.login(username="admin", password="pass")
        data = {
            "name": "Photo Property",
            "property_type": "short-term",
            "location": "City",
            "description": "Pics",
            "guests": 1,
            "bedrooms": 1,
            "bathrooms": 1,
        }
        photo = SimpleUploadedFile("test.jpg", b"abc", content_type="image/jpeg")
        response = self.client.post(
            reverse("add_property"), {**data, "photos": [photo]}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        prop = Property.objects.get(name="Photo Property")
        self.assertTrue(prop.photos.exists())

    def test_responsible_field_hidden_without_permission(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("add_property"))
        self.assertNotContains(response, "id_responsible")

    def test_responsible_field_visible_with_permission(self):
        permission = Permission.objects.get(codename="assign_responsible")
        self.admin.user_permissions.add(permission)
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("add_property"))
        self.assertContains(response, "id_responsible")


class SearchTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.p1 = Property.objects.create(
            name="Lake House",
            property_type="short-term",
            location="Lakeview",
            description="Nice",
            guests=4,
            bedrooms=2,
            bathrooms=1,
        )
        self.p2 = Property.objects.create(
            name="City Loft",
            property_type="short-term",
            location="Downtown",
            description="Cool",
            guests=2,
            bedrooms=1,
            bathrooms=1,
        )
        Booking.objects.create(
            property=self.p1,
            user=self.user,
            start_date="2024-06-10",
            end_date="2024-06-15",
            status="booked",
        )

    def test_search_excludes_booked(self):
        params = {
            "type": "short-term",
            "checkin_iso": "2024-06-12",
            "checkout_iso": "2024-06-14",
            "guests_total": "2",
        }
        url = reverse("properties:property_list") + "?" + urlencode(params)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Lake House")
        self.assertContains(response, "City Loft")

