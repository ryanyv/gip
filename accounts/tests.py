from django.test import TestCase
from django.contrib.auth import get_user_model


class AuthRoutesTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_route_exists(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_logs_out_and_redirects(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/logout/', follow=True)
        self.assertRedirects(response, '/')
        self.assertNotIn('_auth_user_id', self.client.session)


class RegistrationTest(TestCase):
    def test_authenticated_user_redirected_from_register(self):
        User = get_user_model()
        user = User.objects.create_user(username='existing', password='testpass')
        self.client.login(username='existing', password='testpass')
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 302)

    def test_valid_registration_creates_user(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
            'agree_tos': True,
        }
        response = self.client.post('/register/', data, follow=True)
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_registration_shows_errors(self):
        data = {
            'username': 'baduser',
            'password1': 'pass',
            'password2': 'different',
            'agree_tos': False,
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'match', html=False)
