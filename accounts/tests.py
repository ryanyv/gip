from django.test import TestCase
from django.contrib.auth import get_user_model


class AuthRoutesTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_route_exists(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_route_exists(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_has_register_link(self):
        response = self.client.get('/login/')
        self.assertContains(response, 'href="/register/"')

    def test_logout_logs_out_and_redirects(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/logout/', follow=True)
        self.assertRedirects(response, '/')
        self.assertNotIn('_auth_user_id', self.client.session)
