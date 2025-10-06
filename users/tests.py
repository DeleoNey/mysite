from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Profile

class UserRegistrationTest(TestCase):

    def test_user_registration(self):
        response = self.client.post('/users/register/', {
            'username': 'newuser',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'email': 'newuser@example.com',
            'first_name': 'Іван',
            'last_name': 'Іванов'
        })
        self.assertEqual(response.status_code, 302)  # перенаправлення після успішної реєстрації
        user = User.objects.get(username='newuser')
        self.assertEqual(user.first_name, 'Іван')
        self.assertEqual(user.last_name, 'Іванов')
        self.assertTrue(Profile.objects.filter(user=user).exists())

class UserProfileUpdateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', first_name='Old', last_name='User')
        self.client.login(username='testuser', password='12345')

    def test_profile_update(self):
        response = self.client.post('/users/profile/edit/', {
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
            'email': 'testuser@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()  # <- оновлюємо дані з БД
        self.assertEqual(self.user.first_name, 'NewFirst')
        self.assertEqual(self.user.last_name, 'NewLast')
