# praktikum_new_diplom
![foodgram-project-react Workflow Status](https://github.com/umv17/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master&event=push)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
## Описание проекта Foodgram
«Продуктовый помощник»: приложение, на котором пользователи публикуют рецепты,
подписываться на публикации других авторов и добавлять рецепты в избранное. 
Сервис «Список покупок» позволит пользователю создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

[Пример сервера](https://umika.ddns.net/)

## Проект включает 5 сервисов:
- backend - образ backend проекта
- frontend - образ frontend проекта
- postgres - образ базы данных PostgreSQL
- nginx - образ web сервера nginx
- certbot - образ для работы с https

## Установить docker, docker-compose на сервере:
```bash
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
-Перенести файлы docker-compose.yml и default.conf на сервер.

```bash
scp docker-compose.yml username@server_ip:/home/<username>/
scp nginx.conf <username>@<server_ip>:/home/<username>/
```

- Создайте файл ".env" и заполнить в настройках репозитория секреты .env

```python
DB_ENGINE='django.db.backends.postgresql'
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса
DB_PORT=5432 # порт для подключения к БД
```
- запускаем контейнер:

```bash
sudo docker-compose up -d
```
-Первоначальная настройка
```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py load_tags
sudo docker-compose exec backend python manage.py load
```

### Автор:
Михаил Унжаков
