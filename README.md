# _Online Store_
[![Static Badge](https://img.shields.io/badge/Python-blue?style=flat&logo=Python&labelColor=ffff99&color=0066ff)](https://www.python.org)
[![Static Badge](https://img.shields.io/badge/-Django-006400?style=&logo=django)](https://www.djangoproject.com)
[![Static Badge](https://img.shields.io/badge/Django%20Rest%20Framework-white?style=flat&logoColor=800080&labelColor=990000)](https://www.django-rest-framework.org)
[![Static Badge](https://img.shields.io/badge/Swagger-3CB371?logo=swagger&logoColor=black)](https://swagger.io)
![Static Badge](https://img.shields.io/badge/PostgreSQL-blue?style=flat&logo=postgresql&labelColor=white)
![Static Badge](https://img.shields.io/badge/Celery-006400?style=flat&logo=Celery&logoColor=green)
![Static Badge](https://img.shields.io/badge/Redis-ff5050?style=flat&logo=Redis&labelColor=white)
![Static Badge](https://img.shields.io/badge/RabbitMQ-white?style=flat&logo=RabbitMQ)
![Static Badge](https://img.shields.io/badge/Sentry-800080?style=flat&logo=Sentry&logoColor=800080&labelColor=white)

>_Language: [Русский](README.md), [English](README.en.md)_ 

### 📃 Содержание
1. ✏️ [Описание проекта](#project_desc)
   - 📋 [Задачи](#goals)
   - 📟 [Функциональные возможности](#func_abilities)
2. 📱 [Технологии проекта](#project_technologies)
3. 📚 [Используемые зависимости](#dependencies_used)
4. 📈 [Связи между таблицами](#table)
5. 🔌 [Установка и запуск](#installation_and_launch)
   - 📔 [Установка проекта в IDE](#installation_ide)
   - 🐳 [Установка проекта в Docker](#installation_docker)
6. 📗 [Документация API](#documentation_api)
7. 🔐 [Лицензия](#license)

<a name="project_desc"></a> 
## ✏️ Описание проекта ##
Проект на Django Rest Framework, предназначенный показать взаимодействия
"**Онлайн Магазина**" с _Покупателем_, _Менеджером_ / _Админом_ и _Поставщиком_.

<a name="goals"></a>
### 📋 Задачи ###
Проект был разработан с целью изучения Django Rest Framework.\
Были изучены такие темы, как:
- Паттерны _MVC_, _MVP_. ✅
- Аутентификация _JWT_. ✅
- Аутентификация _sessions_. ✅
- Интеграция. ✅
- Регистрация по _SMTP_-протоколу. ✅
- Регистрация, авторизация с помощью _Djoser_. ✅
- Оптимизация с помощью подключения _фоновых задач_. ✅
- Оптимизация с помощью _Кэша_. ✅
- Работа _брокеров очередей_ (Redis, RabbitMQ, Kafka). ✅
- Разница между _RabbitMQ_ и _Kafka_, плюсы и минусы их использования. ✅

<a name="func_abilities"></a> 
### 📟 Функциональные возможности ###
- Users: 💁
  - Регистрация:
    - Регистрация пользователя.
    - Запрос о новом пароле на почту.
  - Авторизация:
    - Смена пароля.
    - Активация пользователя.
    - Сброс пароля.
  - JWT-аутентификация
    - Создание токена.
    - Обновление токена.
    - Проверка токена.
  - Пользователь:
    - Посмотреть профиль 
    - Изменить профиль.
- Categories: 📂
  - Просмотр: 
    - Посмотреть категорию, подкатегорию.
    - Посмотреть список категорий и их подкатегории.
  - Добавление:
    - Добавление категории, подкатегории. (_Админ_ / _Менеджер_)
  - Изменение:
    - Изменение категории, подкатегории. (_Админ_ / _Менеджер_)
  - Удаление:
    - Удаление категории, подкатегории. (_Админ_ / _Менеджер_)
  - Поиск:
    - Поиск по категориям.
    - Поиск по подкатегориям. \[**В разработке**]
- Products: 🍫
  - Просмотр:
    - Посмотреть товар.
    - Посмотреть список товаров.
  - Добавление:
    - Добавить товар. (_Админ_ / _Менеджер_ / _Поставщик_)
  - Изменение:
    - Изменить товар. (_Админ_ / _Менеджер_ / _Поставщик_)
  - Удаление:
    - Удалить товар. (_Админ_ / _Менеджер_ / _Поставщик_)
  - Поиск:
    - Поиск по товарам.
- Providers: 👷
  - Просмотр:
    - Посмотреть поставщика.
    - Посмотреть список поставщиков.
  - Добавление:
    - Добавить поставщика. (_Админ_ / _Менеджер_)
  - Изменение:
    - Изменить поставщика. (_Админ_ / _Менеджер_ / _Поставщик_)
  - Удаление:
    - Удалить поставщика. (_Админ_ / _Менеджер_ / _Поставщик_)
  - Поиск:
    - Поиск по поставщикам.
- Carts: 📲
  - Просмотр:
    - Посмотреть корзину
    - Посмотреть список корзин. (_Админ_ / _Менеджер_)
  - Добавление:
    - Добавить товар в корзину.
  - Изменение:
    - Изменить товар в корзине.
  - Удаление:
    - Удалить товар из корзины.
    - Очистить корзину. \[**В разработке**]
- Orders: 📝
  - Просмотр:
    - Посмотреть заказ.
    - Посмотреть список заказов.
  - Добавление:
    - Оформить заказ.
  - Изменение:
    - Изменение статуса заказа. (_Админ_ / _Менеджер_) \[**В разработке**]
  - Удаление:
    - Удалить заказ.

<a name="project_technologies"></a>
## 📱 Технологии проекта ##
- Схема - `Spectacular`.
- Регистрация - `SMTP`.
- Отправка сообщений - `Djoser`.
- Отслеживание ошибок - `Sentry`.
- Проверка адреса через - `Google Maps`. **(в разработке)**
- Резервная копия Базы Данных - `CeleryBeat`.
- Кэширование и База Данных - `Redis`.
- Фоновые задачи - `Celery`.
- Брокер очередей - `RabbitMQ`.

<a name="dependencies_used"></a>
## 📚 Используемые зависимости ##
- `Python 3.11`
- `Django 4.2.7`
- `djangorestframework 3.14.0`
- `djangorestframework-simplejwt 5.3.0`
- `drf-spectacular 0.26.5`
- `djoser 2.2.2`
- `psycopg2 2.9.9`
- `redis 5.0.1`
- `rabbitmq-server 0.0.1`
- `celery 5.3.6`
- `django-celery-beat 2.5.0`
- `sentry-sdk 1.38.0`

<a name="table"></a>
## 📈 Связи между таблицами ##
![img.png](table.png)

<a name="installation_and_launch"></a>
## 🔌 Установка и запуск ##
> [!WARNING]
> Если на вашем компьютере **есть** всё нижеперечисленное, то можете _пропустить_ это предупреждение.
> - Может понадобиться установка [Sentry](https://sentry.io).
> - Может понадобиться установка [Redis](https://redis.io/docs/install/install-redis/).
> - Может понадобиться установка [RabbitMQ](https://www.rabbitmq.com/#getstarted).

<a name="installation_ide"></a>
### 📔 Установка проекта в IDE ##
- Клонирование репозитория:
```text
git clone https://github.com/AntonVagabond/online_store.git
```
- Создание виртуального окружения и установка зависимостей:
```text
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
- Создание `.env` на основе `.env.example`
```.env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

PG_DATABASE=
PG_USER=
PG_PASSWORD=
DB_HOST=
DB_PORT=

SENTRY_DSN=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=
```

<a name="installation_docker"></a>
### 🐳 Установка проекта в Docker ###
- Билд проекта:
```docker
docker-compose up -d --build
```
- Создание миграций:
```docker
docker exec web python manage.py makemigrations
```
- Применение миграций:
```docker
docker exec web python manage.py migrate
```
- Инициализация проекта:
```docker
docker-compose exec make initial
```
- Добавление superuser-а:
```
docker-compose exec web python manage.py createsuperuser
```

<a name="documentation_api"></a>
## 📗 Документация API ##
Документация по API доступна по `/api/v1`.

<a name="license"></a>
## 🔐 Лицензия ##
Подробности см. в файле LICENSE.