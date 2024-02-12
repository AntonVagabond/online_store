# ------------------------------------- VENV ----------------------------------------
# Установка виртуального окружения.
venv:
	python -m venv venv

# Активация виртуального окружения.
activate:
	source venv/bin/activate
# -----------------------------------------------------------------------------------


# --------------------------------- REQUIREMENTS ------------------------------------
# Установка зависимостей проекта.
install:
	pip install -r requirements.txt
# -----------------------------------------------------------------------------------


# ----------------------------- MIGRATIONS AND STATIC -------------------------------
# Применить миграции и отправить.
migrations:
	python ./manage.py makemigrations
	python ./manage.py migrate

# Сбор статик файлов.
static:
	python ./manage.py collectstatic
# -----------------------------------------------------------------------------------


# ----------------------------------- LOAD DATA -------------------------------------
# Загрузить данные в базу данных.
load:
	python ./manage.py loaddata fixtures/categories.json
	python ./manage.py loaddata fixtures/providers.json
	python ./manage.py loaddata fixtures/products.json
	python ./manage.py loaddata fixtures/products_description.json
	python ./manage.py loaddata fixtures/products_feature.json
	python ./manage.py loaddata fixtures/products_images.json
# -----------------------------------------------------------------------------------


# ------------------------------------- SUPERUSER -----------------------------------
# Создание суперпользователя.
createsuperuser:
	python ./manage.py createsuperuser
# -----------------------------------------------------------------------------------


# ------------------------------ RUN AND STOP SERVER --------------------------------
# Запуск сервера разработки.
run:
	python manage.py runserver

# Остановка сервера разработки.
stop:
	pkill -f "python ./manage.py runserver"
# -----------------------------------------------------------------------------------


# ------------------------------------- CELERY --------------------------------------
# Запустить Celery. Убедитесь в том, что у вас запущен Redis (на WSL2, если
# у вас Windows) и RabbitMQ на вашем локальном хосте!
celery:
	celery --app=config worker --loglevel=info --pool=solo

# Запустить Celery Beat для резервной копии Базы Данных.
beat:
	celery -A config beat -l info
# -----------------------------------------------------------------------------------