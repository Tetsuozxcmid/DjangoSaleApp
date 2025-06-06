# DjangoSaleApp - сервис объявлений пользователей

![Django](https://img.shields.io/badge/Django-5.2-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12.5+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

> Платформа для размещения объявлений с системой обмена товарами между пользователями

## Содержание
- [Установка](#Установка)
- [Пояснение](#Пояснение)
- [Возможности](#Возможности)
- [Тестирование](#Тестирование)
- [Использование](#Использование)
- [API Endpoints](#Эндпоинты)



## Установка
Создать пустую папку с любым именем, Пример ```djangoapp```
### Требования
- Python 
- Django 
- Sqlite

### Запуск
```bash
# Клонирование репозитория
git clone https://github.com/Tetsuozxcmid/DjangoSaleApp


```

# Настройка окружения
Переходим в терминал проекта и создаем окружение
```
python -m venv venv

venv/scripts/activate

cd DjangoSaleApp
cd auth_system
```  

# Установка зависимостей
```pip install -r requirements.txt```

# Миграции и запуск
```

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```
будет доступен сервер по адресу ``` http://127.0.0.1:8000/ ``` на локальном порту


### Пояснение
При выполнении команды 
```python manage.py migrate``` происходит миграция сущностей

- User (```django.contrib.auth.models```):
    - Username: username пользователя
    - Password: пароль пользователя (кодируется)
     
- Post: 
    - title: Название обьявления
    - Description: Описание обьявления
    - Category: Категория товара в обьявлении на выбор из choices ```('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('furniture', 'Мебель'),
        ('other', 'Другое')```
    - Condition: Состояние товара в обьявлении на выбор из choices ``` ('new', 'Новый'),
        ('used', 'Б/У') ```

     - Created_at: Дата создания публикации 
     - Author: Идет связь с айдишником юзера который создал этот пост Внешним ключом

- Offer
    - sender_user: связь с юзером который отправил предложение об обмене
    - ad_receiver: связь с обьявление на которое откликнулся юзер внешним ключом
    - comment: сопроводительное сообщение на отклик обмена в котором юзер пишет на что он хочет произвести обмен
    - status: Статус предложения, берется из choices ( по дефолту - ```pending - ожидает ```) choices ```('await', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отказано')```
    - Created_at: Время отправки предложения 



## О проекте

DjangoSaleApp - это веб-платформа для размещения объявлений с уникальной системой обмена товарами между пользователями

## Возможности

###  Система пользователей
- Валидация данных на стороне сервера
  - Проверка уникальности имени пользователя
  - Шифрование паролей (Django PBKDF2)
    -   (logout) с очисткой сессии
      
![Регистрация](https://github.com/Tetsuozxcmid/DjangoSaleApp/blob/main/auth_system/accounts/docs/Страница-регистрации.png?raw=true)


#### Личный кабинет
- Просмотр всех действующих предложений об обмене
- Управление входящими предложениями обмена
- История действий с объявлениями
  
![Предложения](https://github.com/Tetsuozxcmid/DjangoSaleApp/blob/main/auth_system/accounts/docs/Предложение-обмена.png?raw=true)

### Система обьявлений

- Создание постов обьявлений через кастомную форму
- Возможность удалять/редактировать только с проверкой user.id == post.author (чужой пост удалить или редактировать нельзя) 
**Удаление объявлений**:
  - Каскадное удаление связанных предложений
  - Мгновенное обновление UI после удаления
    
  ![Главная страница](https://github.com/Tetsuozxcmid/DjangoSaleApp/blob/main/auth_system/accounts/docs/Главная-страница.png?raw=true)

### Система предложений об обмене 
- Создание предложений об обмене через кастомную форму
- Сверка какому обьявлению от какого юзера было послано предложение об обмене
- Автоматически при отправке предложения , оффер становится в статус pending('ожидание') и должен быть либо принят либо отказан через свой кабинет пользователя которому пришел обмен

### Использование
- При создании сервера ```python manage.py runserver ``` будет доступен сервер по адресу ``` http://127.0.0.1:8000/ ``` на локальном порту, дальше при переходе на главную страницу, если юзер не аутенфицирован - будет страница с регистрацией, юзер заносится в бд
  
    - сразу после этого происходит redirect на страницу логина где нужно ввести указанные в регистрации данные, происходит проверка данных с данными из бд которые были указаны при регистрации, в случае корректности введенных данных происходит переброс на основную страницу
- На основной странице есть Кнопки "Создать пост", "Мои предложения","Выйти".
    - При создании поста нужно указать его title,Description,Category,Condition и опубликовать пост, после этого пост будет создан на главной странице

    - При выборе "Мои предложения" перебросит на страницу предложений, где можно будет увидеть кто , когда и какое предложение вам кидал. Для тестирования можно запустить python manage.py test либо создать второго пользователя и откликнуться на ранее созданный первым пользователем пост и указать на что вы хотите обменять в сопроводительном сообщении. После этого в кабинете первого юзера появится отправленное вторым юзером предложение обмена

    - "Выйти" простой логаут из сессии

# Эндпоинты

##  Аутентификация и авторизация

| Endpoint | Метод | Функционал | Особенности | Доступ |
|----------|-------|------------|-------------|--------|
| `/` | GET | Перенаправление на страницу входа | Редирект на `auth_login` | Все |
| `/register/` | GET | Форма регистрации | - | Все |
|  | POST | Создание пользователя | Валидация данных, хеширование пароля | Все |
| `/login/` | GET | Форма входа | - | Все |
|  | POST | Аутентификация | Проверка логина/пароля, создание сессии | Все |
| `/logout/` | GET | Выход из системы | Очистка сессии | Авторизованные |

##  Управление объявлениями

| Endpoint | Метод | Функционал | Особенности | Доступ |
|----------|-------|------------|-------------|--------|
| `/welcome/` | GET | Главная страница | Сортировка по дате (новые сначала) | Авторизованные |
| `/posts/create/` | GET | Форма создания | - | Авторизованные |
|  | POST | Сохранение объявления | Привязка к текущему пользователю | Авторизованные |
| `/posts/edit/<int:post_id>/` | GET | Форма редактирования | - | Авторизованные (только автор) |
|  | POST | Обновление объявления | Проверка прав автора | Авторизованные (только автор) |
| `/posts/delete/<int:post_id>/` | GET | Удаление объявления | Каскадное удаление предложений | Авторизованные (только автор) |

##  Система обмена

| Endpoint | Метод | Функционал | Особенности | Доступ |
|----------|-------|------------|-------------|--------|
| `/post/<int:post_id>/exchange/` | GET | Форма предложения обмена | - | Авторизованные |
|  | POST | Создание предложения | Проверка "не свое объявление" | Авторизованные |
| `/my-offers/` | GET | Просмотр предложений | Фильтрация по получателю | Авторизованные |
| `/my-offers/accept/<int:offer_id>/` | POST | Принятие предложения | Смена статуса на "принято" | Авторизованные |
| `/my-offers/reject/<int:offer_id>/` | POST | Отклонение предложения | Смена статуса на "отклонено" | Авторизованные |

##  Поиск

| Endpoint | Метод | Функционал | Особенности | Доступ |
|----------|-------|------------|-------------|--------|
| `/search/` | GET | Поиск объявлений | По названию и описанию, регистронезависимый | Все |

### Тестирование
Тестирование проекта можно выполнить командой ```python manage.py test``` находясь в каталоге проекта auth_system

  # Тест аутенфикации пользователей 
  ```Python
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
```
# Тест Создания обьявлений и поиска в поисковой строке
```Python
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
```
# Тест отправления предложений об обмене

```Python
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
```

##  Особенности безопасности
- Все модифицирующие операции требуют авторизации
- Проверка прав доступа к редактированию/удалению
- CSRF-токены для всех форм
- Хеширование паролей


