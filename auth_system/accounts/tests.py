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
        self.user = User.objects.create_user(
            username='testuser', password='pass1234')

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'strongpass123',
            'password2': 'strongpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, 302)


class PostCreatesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.post_create_url = reverse('create_post')
        self.user = User.objects.create_user(
            username='testpostuser', password='pass12345')

    def test_create_post(self):

        self.client.login(username='testpostuser', password='pass12345')

        response = self.client.post(self.post_create_url, {
            'title': 'Тестовое обьявление',
            'description': 'Описание для теста',
            'category': 'clothing',
            'condition': "new",
        })

        self.assertEqual(response.status_code, 302)
        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors)
        from .models import Post
        self.assertTrue(Post.objects.filter(
            title='Тестовое обьявление').exists())

        post = Post.objects.get(title='Тестовое обьявление')
        self.assertEqual(post.author, self.user)
