# Проект **Foodgram** - "Продуктовый помощник"

[![Yambd_final workflow](https://github.com/anthony-bogi/foodgram-project-react/actions/workflows/foodgram_workflows.yml/badge.svg)](https://github.com/anthony-bogi/foodgram-project-react/actions/workflows/foodgram_workflows.yml)

### Автор:

Богданович Антон [anthony-bogi](https://github.com/anthony-bogi)


**«Продуктовый помощник»**: онлайн платформа, где энтузиасты кулинарии делятся своими рецептами, сохраняют понравившиеся рецепты в персональной коллекции и следят за новыми публикациями авторов-кулинаров. Благодаря функции *«Список Покупок»*, участники могут легко составлять список всех необходимых продуктов для приготовления выбранных блюд.

## Используемые технологии

Python 3.7

Django 3.2

Django REST Framework

Djoser

React

PostgreSQL

Docker

Nginx

Gunicorn

Docker


## Запуск приложения на локальной машине:

Склонируйте репозиторий на свой компьютер:

```sh
git clone git@github.com:anthony-bogi/foodgram-project-react.git
```

Перейдите в корневую папку:

```sh
cd foodgram-project-react/
```

А затем в папку с инфраструктурой проекта:

```sh
cd infra/
```

Создайте файл ".env" и заполните своими данными по примеру:

```sh
SECRET_KEY=<...>  # Секретный ключ (settings.py)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Запустите сборку контейнеров:

```sh
docker-compose up -d --build
```

Выполните миграции:

```sh
docker-compose exec web python manage.py migrate
```

Создайте суперпользователя:

```sh
docker-compose exec web python manage.py createsuperuser
```

Соберите статику:

```sh
docker-compose exec web python manage.py collectstatic --no-input
```

Загрузите базу ингредиентов:

```sh
docker-compose exec web python manage.py load_ingredients_csv
```

После удачных действий проект должен быть доступен по адресу: [http://localhost/](http://localhost/)

А документация должна быть доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)

Для остановки приложения в контейнерах Docker без удаления:

```sh
docker-compose stop
```

Для остановки приложения в контейнерах Docker с их удалением:

```sh
docker-compose down -v
```

Далее необходимо зайти через админ-панель проекта [http://localhost/admin/](http://localhost/admin/) и добавить теги для рецептов. Теги добавляются только админом и являются обязательными для сохранения рецепта. Теги также используются для фильтрации рецептов.

Если нужно снова запустить контейнеры:

```sh
docker-compose start
```

## Запуск приложения на удаленном сервере:

Склонируйте репозиторий:

```sh
git clone git@github.com:anthony-bogi/foodgram-project-react.git
```

Зайдите на сервер и остановите службу nginx:

```sh
sudo systemctl stop nginx
```

Установите Docker и Docker Compose:

```sh
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt-get install docker-compose-plugin
```

Или проверьте установленные версии:

```sh
docker version
docker-compose version
```

В файле ../infra/nginx.conf в локальном репозитории замените данные в строке server_name на IP-адрес удаленного сервера.

Скопируйте на сервер файлы docker-compose.yml и nginx.conf:

```sh
scp docker-compose.yml nginx.conf username@IP:/home/username/
```

>где *username* - это имя пользователя на сервере, а *IP* - публичный IP-адрес сервера

В репозитории проекта на Github в разделе Settings > Secrets > Actions создайте переменные окружения.

Запустите сборку контейнеров:

```sh
sudo docker compose up -d --build
```

Выполните миграции:

```sh
sudo docker compose exec web python manage.py migrate
```

Создайте суперпользователя:

```sh
sudo docker compose exec web python manage.py createsuperuser
```

Соберите статику:

```sh
sudo docker compose exec web python manage.py collectstatic --no-input
```

Загрузите базу ингредиентов:

```sh
sudo docker compose exec web python manage.py load_ingredients_csv
```

Можно зайти на сайт по введенному IP-адресу и посмотреть результат.

Для остановки приложения в контейнерах Docker без удаления:

```sh
sudo docker compose stop
```

Для остановки приложения в контейнерах Docker с их удалением:

```sh
sudo docker compose down -v
```

После каждого push в ветку master репозитория (его обновления) можно зайти на вкладку Actions на GitHub и проверить все действия workflow:

- Проверка кода с использованием пакета flake8 для соблюдения стандарта PEP8.
- Создание и загрузка Docker-образов frontend и backend (web) на Docker Hub.
- Развертывание проекта на удаленном сервере.
- Отправка уведомления в Telegram в случае успешного выполнения всех действий.

## Требования:

```sh
asgiref==3.7.2
certifi==2023.5.7
cffi==1.15.1
charset-normalizer==3.1.0
coreapi==2.3.3
coreschema==0.0.4
cryptography==41.0.1
defusedxml==0.7.1
Django==3.2.19
django-filter==23.2
django-templated-mail==1.1.1
djangorestframework==3.14.0
djangorestframework-simplejwt==4.7.2
djoser==2.1.0
drf-extra-fields==3.5.0
filetype==1.2.0
flake8==5.0.4
flake8-broken-line==0.6.0
flake8-isort==6.0.0
flake8-plugin-utils==1.3.3
flake8-return==1.2.0
gunicorn==20.1.0
idna==3.4
importlib-metadata==1.7.0
isort==5.11.5
itypes==1.2.0
Jinja2==3.1.2
MarkupSafe==2.1.3
mccabe==0.7.0
oauthlib==3.2.2
pep8-naming==0.13.3
Pillow==9.5.0
psycopg2-binary==2.8.6
pycodestyle==2.9.1
pycparser==2.21
pyflakes==2.5.0
PyJWT==2.7.0
python-dotenv==0.21.1
python3-openid==3.2.0
pytz==2023.3
reportlab==4.0.4
requests==2.31.0
requests-oauthlib==1.3.1
six==1.16.0
social-auth-app-django==4.0.0
social-auth-core==4.4.2
sqlparse==0.4.4
typing_extensions==4.6.3
uritemplate==4.1.1
urllib3==2.0.3
zipp==3.15.0
```

## Доступ для проверки проекта:

IP: [84.201.167.51](http://84.201.167.51/)

Доменное имя: [http://foodgrambyanthony.ddns.net/](http://foodgrambyanthony.ddns.net/)


Далее для проверки работоспособности сайта через админ-панель заходим по ссылке:

- [http://foodgrambyanthony.ddns.net/admin/](http://foodgrambyanthony.ddns.net/admin/)

или

- [http://84.201.167.51/admin/](http://84.201.167.51/admin/)

Вводим логин (по email) и пароль администратора:

```sh
email: admin@admin.ru
password: mainadmin666

# login: admin
```
