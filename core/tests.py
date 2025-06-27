from django.test import TestCase
from django.urls import reverse
from properties.models import Property


class HomeViewTests(TestCase):
    def test_home_displays_featured_property(self):
        Property.objects.create(
            name="Home Test Property",
            property_type="short-term",
            location="Test Location",
            description="desc",
            is_featured=True,
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home Test Property")

