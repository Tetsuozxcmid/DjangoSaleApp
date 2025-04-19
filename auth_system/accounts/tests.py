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
        self.post_delete_url = reverse('delete_post', args=[1])
        self.post_edit_url = reverse('edit_post', args=[1])
        self.post_search_url = reverse('search')

        self.user = User.objects.create_user(
            username='testpostuser', password='pass12345')

        self.post = Post.objects.create(
            title='Тестовое обьявление для удаления',
            description='Описание для удаления',
            category='clothing',
            condition='new',
            author=self.user
        )

    def test_create_post(self):
        self.client.login(username='testpostuser', password='pass12345')

        response = self.client.post(self.post_create_url, {
            'title': 'Тестовое обьявление',
            'description': 'Описание для теста',
            'category': 'clothing',
            'condition': 'new',
        })

        self.assertEqual(response.status_code, 302)
        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors)

        from .models import Post
        self.assertTrue(Post.objects.filter(
            title='Тестовое обьявление').exists())

        post = Post.objects.get(title='Тестовое обьявление')
        self.assertEqual(post.author, self.user)

    def test_delete_post(self):
        self.client.login(username='testpostuser', password='pass12345')

        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

        response = self.client.post(self.post_delete_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_edit_post(self):
        self.client.login(username='testpostuser', password='pass12345')
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

        response = self.client.post(self.post_edit_url, {
            'title': 'Изменённый заголовок',
            'description': 'Обновлённое описание',
            'category': 'electronics',
            'condition': 'used',
        })
        self.assertEqual(response.status_code, 302)

        self.post.refresh_from_db()

        self.assertEqual(self.post.title, 'Изменённый заголовок')

        self.assertEqual(self.post.description, 'Обновлённое описание')

        self.assertEqual(self.post.category, 'electronics')

        self.assertEqual(self.post.condition, 'used')

        self.assertEqual(self.post.author, self.user)

    def test_search_post(self):
        self.client.login(username='testpostuser', password='pass12345')
        Post.objects.create(
            title='Автомобиль',
            description='Продаю авто',
            category='other',
            condition='used',
            author=self.user
        )

        response = self.client.post(self.post_search_url, {
            'title': 'Автомобиль'
        })

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Автомобиль')


class OfferCreateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender_user = User.objects.create_user(
            username='senderuser', password='testpass')
        self.receiver_user = User.objects.create_user(
            username='receiveruser', password='testpass')

        self.receiver_post = Post.objects.create(
            title='Ноутбук',
            description='Новый ноутбук',
            category='electronics',
            condition='new',
            author=self.receiver_user
        )

        self.offer_url = reverse('create_exchange', args=[
                                 self.receiver_post.id])

    def test_create_offer_success(self):
        self.client.login(username='senderuser', password='testpass')

        response = self.client.post(self.offer_url, {
            'ad_receiver': self.receiver_post.id,
            'comment': 'Хочу обменять на что-то другое'
        })

        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)

        from .models import Offer
        self.assertTrue(Offer.objects.filter(
            sender_user=self.sender_user,
            ad_receiver=self.receiver_post,
            comment='Хочу обменять на что-то другое'
        ).exists())
