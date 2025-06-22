from django.test import TestCase


class AuthRoutesTest(TestCase):
    def test_login_route_exists(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_route_exists(self):
        response = self.client.get('/logout/')
        # A GET request may require POST and return 405, but the path should exist.
        self.assertNotEqual(response.status_code, 404)
