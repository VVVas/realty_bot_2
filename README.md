# Бот для телеграм, в котором пользователи находят коммерческие площади для своего бизнеса.  

## Это продолжение разработки бота после хакатона.  

## Как пользоваться
Найдите в ТГ бота  

Выберите город, категорию, диапазон стоимости и получите объявления о недвижимости.  
Если объявлений по запрошенным параметрам нет, то вы получите сведения об объектах недвижимости в выбранном городе и категории.  

Объявления можно добавлять в своё Избранное.  
Оставляйте комментарий к объявлениям, которые будут видны после одобрения администратором, — это позволит оперативно обновить информацию в объявлении.  

## Инструкции  

Создайте пользователя в административном разделе на сайте, дайте ему статус персонала и добавьте в группу «Администратор».  
Подробнее в [видеоинструкции](https://youtu.be/pqCblYN6W84).  

В административном разделе на сайте можно добавлять объекты недвижимости и создавать объявления в объектах недвижимости.  

Можно отредактировать сообщения бота прямо из административного раздела.  

Одобряйте комментарии пользователей — это позволит узнавать актуальную информацию от тех кто посмотрел объект объявления «в живую».  

После запуска бот имеет стартовый набор городов и категорий, что позволит сразу создать объекты недвижимости и объявления.

## Как развернуть локально
Установите локально Docker.  
Перейдите в директорию `infra`.  
Создайте файл `.env` и заполните его по образцу `.env.example`.  
Запустите докер:  
```
docker compose up --build  
```

Применение миграций в контейнере:  
```
docker compose exec backend python manage.py migrate  
```

Сборка статических файлов в контейнере (стили для админки):  
```
docker compose exec backend python manage.py collectstatic --no-input  
```

Импорт стартовых данных:  
```
docker compose exec backend python manage.py admin_permissions_set
docker compose exec backend python manage.py cities_import
docker compose exec backend python manage.py categories_import
docker compose exec backend python manage.py botmessage_import
```

Создание суперпользователя:  
```
docker compose exec backend python manage.py createsuperuser  
```

## Как развернуть на сервере
Установите на сервер Docker и nginx.  
Пробросьте запросы от внешнего nginx к nginx в контейнере.  
Создайте файл `.env` и заполните его по образцу `.env.example`.  
Скопируйте на сервер `.env` и `docker-compose.prod.yml`.  
Запустите докер:  
```
docker compose -f docker-compose.prod.yml up -d  
```

Применение миграций в контейнере:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate  
```

Сборка статических файлов в контейнере (стили для админки):  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --no-input  
```

Импорт стартовых данных:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py admin_permissions_set
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
Создайте суперпользователя выполнив на сервере:  
```
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser  
```

## Стек технологий
Python 3.11, Django 5.0, PTB 21.2, Docker 26.1, nginx 1.26, PostgreSQL 16.3  

## Код написал 
[Мишустин Василий](https://github.com/VVVas), v@vvvas.ru   

## Код предыдущей версии для хакатона написали
[Кавтырев Максим](https://github.com/h-inek)  
[Мишустин Василий](https://github.com/VVVas), v@vvvas.ru, в том числе выполнял роль тим-лида   
[Песчанов Никита](https://github.com/ItWasCain)  
[Сулайманова Сайкал](https://github.com/saikal12)  
[Турубанов Евгений](https://github.com/eturubanov)  
