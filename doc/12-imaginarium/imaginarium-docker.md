# Контейнеризируем приложение.
      
Наше приложение имеет следующую структуру.

![start page]({path-to-subject}/images/10.png)

Как видим оно состоит из 4 запущенных процессов.

Нам необходимо положить каждый процесс в отдельный контейнер и при необходимости пробросить порт некоторых наружу локальной машины.

Начнем с Джанго сервера.

Подготовим requirements.txt с зависимостями.

    Django
    python-socketio
    eventlet
    django-grappelli
    django-debug-toolbar
    django-debug-panel
    Pillow
    redis

Создадим папку docker и в ней файл Dockerfile.django, описывающий образ контейнера с Python и Django.

    FROM python:3.7-slim
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /app
    WORKDIR /app
    COPY requirements.txt /app
    RUN pip install -r requirements.txt
    ENTRYPOINT ["python3.7", "manage.py", "runserver"]
    CMD ["0.0.0.0:8080"]

**0.0.0.0** - обязательно к добавлению в команду для того, чтобы Джанго слушало порт на всех сетевых интерфейсах а не только на локалхосте. Иначе порт не прокидывается наружу.

Запускаем сборку образа

    
    docket build -f docker/Dockerfile.django .


**-f docker/Dockerfile.django** - тут мы указываем источник за пределами текущей директории

Создадим сборщик docker-compose.yaml

    version: '3.5'
    services: 
        django:
            build:
                context: .
                dockerfile: docker/Dockerfile.django
            restart: always
            ports:
                - 8080:8080
            volumes:
                - .:/app
            networks:
                - backend
            container_name: django-server

    networks:
        backend:
            driver: bridge

Запустим контейнер

    docker-compose up

Можно собрать более компактный образ на alpine и поставить в него Python так.

    FROM alpine:3.7
    RUN apk add python3
    RUN apk add py3-pip && \
    pip3 install django && \
    apk del py3-pip


Создадим образ под сокет-сервер Dockerfile.socket.

    FROM python:3.7-slim
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /app
    WORKDIR /app
    COPY requirements.txt /app
    RUN pip install -r requirements.txt
    ENTRYPOINT ["python3.7", "manage.py", "socket_server"]

Добавим контейнер в сборщик docker-compose.yaml.

    version: '3.5'
    services: 
        django:
            build:
                context: .
                dockerfile: docker/Dockerfile.django
            restart: always
            ports:
                - 8080:8080
            volumes:
                - .:/app
            networks:
                - backend
            container_name: django-server

        socket-server:
            build:
                context: .
                dockerfile: docker/Dockerfile.socket
            restart: always
            ports:
                - 5000:5000
            volumes:
                - .:/app
            networks:
                - backend
            container_name: socket-server

    networks:
        backend:
            driver: bridge

Создадим аналогичный образ под sender.

    FROM python:3.7-slim
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /app
    WORKDIR /app
    COPY requirements.txt /app
    RUN pip install -r requirements.txt
    ENTRYPOINT ["python3.7", "sender.py"]

И добавим его в сборщик.

    ...

        sender:
            build:
                context: .
                dockerfile: docker/Dockerfile.sender
            restart: always
            volumes:
                - .:/app
            networks:
                - backend
            container_name: sender

    ...

Однако после запуска получаем ошибку отправки сообщений в редис т.к. изнутри контейнера это пока невозможно.

![start page]({path-to-subject}/images/11.png)

Поэтому нехватает контейнера с Redis.

Его можно создать исключительно в docker-compose из готового образа.

    redis:
        image: "redis:alpine"
        container_name: redis
        networks:
            - backend

Менаяем подключение к Redis.

    mgr = socketio.RedisManager('redis://redis:6379/0')




