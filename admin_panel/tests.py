from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from properties.models import Property

class DeletePropertyTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='admin', password='pass', role='admin')
        self.user = User.objects.create_user(username='user', password='pass')
        self.prop = Property.objects.create(
            name='Test',
            property_type='short-term',
            location='Loc',
            description='Desc',
            guests=1,
            bedrooms=1,
            bathrooms=1,
            responsible=self.admin
        )

    def test_non_admin_cannot_delete(self):
        self.client.login(username='user', password='pass')
        url = reverse('admin_panel_delete_property', args=[self.prop.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Property.objects.filter(id=self.prop.id).exists())

    def test_admin_can_delete(self):
        self.client.login(username='admin', password='pass')
        url = reverse('admin_panel_delete_property', args=[self.prop.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Property.objects.filter(id=self.prop.id).exists())
