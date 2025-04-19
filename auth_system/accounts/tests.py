from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Offer

# Create your tests here.

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.user = User.objects.create_user(username='testuser', password='pass1234')

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'strongpass123',
            'password2': 'strongpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        User.objects.create_user(username='newuser', password='strongpass123')
        response = self.client.post(self.login_url, {
            'username': 'newuser',
            'password': 'strongpass123'
        })
        self.assertEqual(response.status_code, 302)