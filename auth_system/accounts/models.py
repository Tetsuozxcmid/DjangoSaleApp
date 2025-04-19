from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    CATEGORIES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('furniture', 'Мебель'),
        ('other', 'Другое'),
    ]

    CONDITIONS = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]

    title = models.CharField(max_length=180, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание товара')
    category = models.CharField(
        max_length=20, choices=CATEGORIES, verbose_name='Категория')
    condition = models.CharField(
        max_length=20, choices=CONDITIONS, verbose_name='Состояние товара')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title


class Offer(models.Model):
    STATUS = [
        ('await', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отказано'),
    ]

    sender_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_offers')
    ad_receiver = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='received_offers')
    comment = models.TextField(verbose_name='Comment')
    status = models.CharField(max_length=10, choices=STATUS, default='Ожидает')
    created_at = models.DateTimeField(auto_now_add=True)
