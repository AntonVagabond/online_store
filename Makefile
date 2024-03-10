# ------------------------------------- INIT ----------------------------------------
.PHONY: init
init:
# Установка виртуального окружения.
	python -m venv venv
# Активация виртуального окружения.
	source venv/bin/activate
# Установка зависимостей проекта.
	pip install -r requirements.txt
# -----------------------------------------------------------------------------------


# ----------------------------- MIGRATIONS AND STATIC -------------------------------
# Применить миграции и отправить.
.PHONY: migrations
migrations:
	python ./manage.py makemigrations
	python ./manage.py migrate

# Сбор статик файлов.
.PHONY: static
static:
	python ./manage.py collectstatic
# -----------------------------------------------------------------------------------


# ----------------------------------- LOAD DATA -------------------------------------
# Загрузить данные в базу данных.
.PHONY: load
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
.PHONY: createsuperuser
createsuperuser:
	python ./manage.py createsuperuser
# -----------------------------------------------------------------------------------


# ------------------------------ RUN AND STOP SERVER --------------------------------
# Запуск сервера разработки.
.PHONY: run
run:
	python manage.py runserver

# Остановка сервера разработки.
.PHONY: stop
stop:
	pkill -f "python ./manage.py runserver"
# -----------------------------------------------------------------------------------


# ------------------------------------- CELERY --------------------------------------
# Запустить Celery. Убедитесь в том, что у вас запущен Redis (на WSL2, если
# у вас Windows) и RabbitMQ на вашем локальном хосте!
.PHONY: celery
celery:
	celery --app=config worker --loglevel=info --pool=solo

# Запустить Celery Beat для резервной копии Базы Данных.
.PHONY: beat
beat:
	celery -A config beat -l info
# -----------------------------------------------------------------------------------