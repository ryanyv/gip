from django.test import TestCase
from django.urls import reverse


class ContactPageTests(TestCase):
    def test_contact_page_loads(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')

    def test_valid_submission_shows_success(self):
        data = {
            'name': 'Tester',
            'email': 'tester@example.com',
            'message': 'Hello',
        }
        response = self.client.post(reverse('contact'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for contacting us')

