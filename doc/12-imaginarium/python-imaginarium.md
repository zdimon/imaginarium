# Игра Imaginarium.
  
## Суть игры.

Игрокам раздается по 6 картинок.

На картинках изображены различные сюжеты.

[например тут](https://www.pinterest.com/luminousmemory/imaginarium/)

[или тут](http://andrew-lebedinsky.com/Imaginarium-Playing-cards)

Один из игроков выбирает изображение и придумывает для него фразу-ассоциацию.

Остальные игроки выбирают по одному изображению, которые, на их взгляд, подходят под заданную ассоциацию.

Когда все игроки выставили свои варианты изображений они открываются для просмотра.

Далее все игроки кроме загадавшего пытаются угадать изображение по его порядковому номеру.

После того, как все сделали выбор идет подсчет баллов.

Балы получает тот, чью картинку выбрали другие вне зависимости угадали они или нет.

В случае угадывания, балы получают оба игрока (тот кто загадал 3 бала, тот кто угадал 1).

В случае неугадывания 1 бал получает автор картинки.

В случае, если картинку угадали все, автор не получает баллов.

Выигрывает тот, кто первым наберет заданное количество баллов.


## Техника.

Данные для игры будем хранить в текстовом файле json в следующем формате:

    {
        "table": [
            {"number": 1, "image": "1.jpeg", "is_true": true},
            {"number": 2, "image": "2.jpeg", "is_true": false},
            {"number": 3, "image": "3.jpeg", "is_true": false}
            {"number": 4, "image": "4.jpeg", "is_true": false}
            {"number": 5, "image": "5.jpeg", "is_true": false}
        ],
        "users": [
            {"sid": "key", "name": "Vova", "account": 12, "is_dealer": true, "cards": [{},{}...]},
            {"sid": "key", "name": "Dima", "account": 12, "is_dealer": false, "cards": [{},{}...]},
            {"sid": "key", "name": "Fedor", "account": 12, "is_dealer": false, "cards": [{},{}...]},
            {"sid": "key", "name": "Lena", "account": 12, "is_dealer": false, "cards": [{},{}...]},
            {"sid": "key", "name": "Gringo", "account": 12, "is_dealer": false, "cards": [{},{}...]},
        ],
        "user_bets": [
            {"name": "Dima", "card_number": 1},
            {"name": "Fedor", "card_number": 2}
        ],
        "status": "start|gessing|end",
        "association": "good food"
        
    }

Приложение будет разбито на 2 части - бекенд и фронтенд.

Бекенд.

- socketio веб-сокет сервер (брокер сообщений)

- Redis - БД для брокера сообщений

- Django - веб-морда с регистрацией, статистикой и игровым полем.

- sqlite3 - БД для Джанго


Фронтенд

- jquery 

## Функциональные блоки фронтенда.

draw_users, draw_board и т.д. - функции оттрисовки или перерисовки частей игрового поля по переданному json

connect - установка веб-сокет соединения

make_association - установка картинки и текста ассоциации ведущим игроком

make_bet - установка варианта игроками

## Функциональные блоки бекенда.

### Веб-сокет вокер

connect - соединение

disconnect - отсоединение

login - авторизация и получение sid

make_association - установка картинки и текста ассоциации ведущим игроком

make_bet - установка варианта игроками

calculate - подсчет очков и переход хода.

### Джанго вокер

game - игровое поле

index - регистрация/авторизация

unlogin - выход

В процессе игры будем периодично передавать по вебсокету (пару раз в сек) базу данных json и на клиенте постоянно перерисовывать игровое поле.

Передавать будем отдельным процессом (программой).

# Краткое описание шагов разработки.


# Шаг 1. Установка Django, стартовой страницы и попытка подсоединения к сокет-серверу.


Установка проекта

    django-admin startproject name

Запуск сервера

    ./manage.py runserver 8080

Создание БД

    ./manage.py migrate



http://localhost:8000/admin


Создать суперпользователя

    ./manage.py createsuperuser

    python manage.py createsuperuser




       const socket = io('ws://localhost:8050', {transports:['websocket']});  
       
       socket.on('connect', () => {
            console.log('connected!');
            socket.on('message', msg => {
                // console.log(msg);
                $('#time').html(msg.time);
            })
       });


# Шаг 2 (бекенд). Построение сокет-сервера с функцией авторизации.

    import socketio
    import eventlet
    eventlet.monkey_patch()
    mgr = socketio.RedisManager('redis://socketio-redis:6379/0')
    sio = socketio.Server(logger=True, engineio_logger=True, cors_allowed_origins='*',async_mode='eventlet',client_manager=mgr)

    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    def test_message(sid, data):
        print('message ', data)
        sio.emit('message', {'data': 'pong'}, broadcast=True, include_self=True)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    if __name__ == '__main__':
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# Шаг 3 (бекенд). Переодичная отправка данных состояния игры.

    import socketio
    mgr = socketio.RedisManager('redis://socketio-redis:6379/0', write_only=True)
    import time
    from datetime import datetime

    while True:
        time.sleep(2)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        mgr.emit('message', data={'time': current_time})


# Шаг 4 (фронтенд). Форма авторизации.

# Шаг 5 (фронтенд). Отрисовка списка игроков и их картинок.  

# Шаг 6 (бекенд). Функция make_association.

# Шаг 7 (фронтенд). Отрисовка картинок ставок. Форма установки ассоциации.

# Шаг 8 (бекенд). Функция make_bet.

# Шаг 9 (бекенд). Функция calculate.

# Шаг 10 (фронтенд). Кнопка выбора ставки.


# Дальнейшие улучшения.

Добавление изображений карт через админ-интерфейс.

Авторизация через соц. сеть.

Создание игровых комнат.

Чат сообщения.

Верстка под мобильные устройства. Звуковое сопровождение событий.




