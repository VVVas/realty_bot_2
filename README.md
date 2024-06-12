# Premium_product_bot_team_2
Чат-бот для поиска помещения для бизнеса (команда Василия)  

## Как пользоваться
Найдите в ТГ бота  

## Как развернуть локально
Установите локально Docker.  
Перейдите в директорию `infra`.  
Создайте файл `.env` и заполните его по образцу `.env.example`.  
Запустите докер:  
```
docker compose up --build  
```

Создание и применение миграций в контейнере:  
```
docker compose exec backend python manage.py makemigrations  
docker compose exec backend python manage.py migrate  
```

Сборка статических файлов в контейнере (стили для админки):  
```
docker compose exec backend python manage.py collectstatic --no-input  
```

Импорт стартовых данных:  
```
docker compose exec backend python manage.py cities_import
docker compose exec backend python manage.py categories_import
docker compose exec backend python manage.py botmessage_import
```

Создание суперпользователя:  
```
docker compose exec backend python manage.py createsuperuser  
```

## Как развернуть на сервере
Установите на сервер Docker и nginx  
Пробросьте запросы от внешнего nginx к nginx в контейнере  
Создайте файл `.env` и заполните его по образцу `.env.example`
Скопируйте на сервер `.env` и `docker-compose.prod.yml`  
Запустите докер:  
```
docker compose -f docker-compose.prod.yml up -d  
```

Создание и применение миграций в контейнере:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py makemigrations  
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate  
```

Сборка статических файлов в контейнере (стили для админки):  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --no-input  
```

Импорт стартовых данных:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py cities_import  
docker compose -f docker-compose.prod.yml exec backend python manage.py categories_import  
docker compose -f docker-compose.prod.yml exec backend python manage.py botmessage_import  
```

Создание суперпользователя:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser  
```

## Как развернуть на сервере из Гитхаба с помощью автоматического воркфлоу  
Установите на сервер Docker и nginx.  
Пробросьте запросы от внешнего nginx к nginx в контейнере.  
В Гитхаб перейдите в `.github/workflows`, в файле `main.yml`:  
- измените названия образов (значение `tags:`) для публикации в DockerHub для бэкэнда и гейтвея.  
- укажите директорию назначения на сервере для копирования `docker-compose.prod.yml` (значение `target`).  
- добавьте значения секретов в настройках репозитария (Settings → Secrets and variables → Actions).  
Создайте файл `.env` и заполните его по образцу `.env.example`.  
Скопируйте на сервер `.env` в директорию для копирования `docker-compose.prod.yml`.  
Одобрите пулреквест в ветку `prod`.  
Создайте суперпользователя на сервере:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser  
```


## Стек технологий
Python 3.11, Django 5.0, PTB 21.2, Docker 26.1, nginx 1.26, PostgreSQL 16.3  

## Авторы
[Кавтырев Максим](https://github.com/h-inek)  
[Мишустин Василий](https://github.com/VVVas), v@vvvas.ru   
[Песчанов Никита](https://github.com/ItWasCain)  
[Сулайманова Сайкал](https://github.com/saikal12)  
[Турубанов Евгений](https://github.com/eturubanov)  

Сделано в Мастерской программирования Яндекс.Практикума под руководством [Александрова Романа](https://github.com/teamofroman) и Гончар Маргариты  
