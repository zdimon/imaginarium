## Авторизация по веб-сокету.
       
Создаем веб-сокет соединение в шаблоне game.html.

    {% extends 'layout.html' %}

    {% block main %}
        <h1> Игра </h1>

        <script>
            const socket = io('ws://localhost:5000', {transports:['websocket']});  
         </script>
    {%  endblock %}

Скрипт сокет-сервера с одним событием.

    import socketio
    import eventlet
    eventlet.monkey_patch()
    mgr = socketio.RedisManager('redis://socketio-redis:6379/0')
    sio = socketio.Server(cors_allowed_origins='*',async_mode='eventlet')

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

Тут мы используем Redis в качестве брокера сообщений для отправки их из произвольного места django приложения внутрь БД Redis а от туда они автоматически будут попадать внутрь запущенного веб-сокет сервера.

Установка библиотеки-клиента.

    pip install redis

Запуск сервера.

    python3 socket_server.py

Теперь нам необходимо отработать 2 функции коннекта и дисконекта и добавлять или удалять идентификатор соединения в обьект пользователя в поле sids.

Для того, чтобы иметь доступ к моделям джанги предлагаю внести сокер-сервер внутрь команды джанги.

Создаем новый файл game/management/commands/socket_server.py

    from django.core.management.base import BaseCommand, CommandError
    from game.models import Gameuser
    from imagin.settings import BASE_DIR

    import socketio
    import eventlet
    eventlet.monkey_patch()
    mgr = socketio.RedisManager('redis://localhost:6379/0')
    sio = socketio.Server(cors_allowed_origins='*',async_mode='eventlet',client_manager=mgr)


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

    class Command(BaseCommand):
        
        def handle(self, *args, **options):
            print('Statrting socket server')
            eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

Теперь пошлем сообщение из браузера и передадим логин пользователя на сервер.

        socket.on('connect', () => {
            socket.emit('login',{login: window.localStorage.getItem('login')});
        });

Пробуем записать в базу sid.

    @sio.event
    def login(sid, data):
        user = Gameuser.objects.get(login=data['login'])
        user.sids = sid
        user.save()

Ошибка конкурентного (паралельного) выполнения.

    django.db.utils.DatabaseError: DatabaseWrapper objects created in a thread can only be used in that same thread. The object with alias 'default' was created in thread id 139889788240096 and this is thread id 139889748609480.

Произошло переключение потоков, в одном потоке создался обьект базы данных а в другом произошла попытка его использовать.

Как вариант можно попроборать создать свой собственный поток и в нем поработать с БД, пробросив необходимые переменные.

    import threading

    def add_user_task(sid,data):
        user = Gameuser.objects.get(login=data['login'])
        user.sids = sid
        user.save()

    @sio.event
    def login(sid, data):
        print('login ', sid)
        print(data)
        thread = threading.Thread(target=add_user_task, args=(sid,data))
        thread.start()

Осталось создать две функции в модели для добавления и удаления sid из объекта user.


    def add_sid(self,sid):
        sids = self.sids.split(';')
        if sid not in sids:
            sids.append(sid)
        self.sids = ';'.join(sids)
        self.save()

    @staticmethod
    def remove_sid(sid):
        user = Gameuser.objects.get(sids__contains=sid)
        sids = user.sids.split(';')
        if sid in sids:
            sids.remove(sid)
        user.sids = ';'.join(sids)
        user.save() 

remove_sid - мы оформили в виде статической функции т.к. при удалении нам известен только sid и мы не можем найти пользователя по логину.


Вызов функций в сокет-сервере.

    def add_user_task(sid,data):
        user = Gameuser.objects.get(login=data['login'])
        user.add_sid(sid)

    def remove_user_task(sid):
        Gameuser.remove_sid(sid)


    @sio.event
    def login(sid, data):
        thread = threading.Thread(target=add_user_task, args=(sid,data))
        thread.start()


    @sio.event
    def disconnect(sid):
        thread = threading.Thread(target=remove_user_task, args=(sid,))
        thread.start()

**TODO:**

Организовать хранение sid соединений в отдельной таблице для упрощения поиска.

## Отслеживание пользователей онлайн

Добавим новое поле в модель пользователей и проведем миграцию.

    class Gameuser(models.Model):
        ....
        is_online = models.BooleanField(default=False)

Добавим функцию проверки пользователей онлайн и задействуем ее в модели.

    class Gameuser(models.Model):
        ...
        is_online = models.BooleanField(default=False)

        def add_sid(self,sid):
            ...
            self.check_online()

        @staticmethod
        def remove_sid(sid):
            .... 
            for u in Gameuser.objects.all():
                u.check_online()     

        def check_online(self):
            if(len(self.sids)>5):
                self.is_online = True
            else:
                self.is_online = False
            self.save()

Теперь отследим изменение поля is_online и если оно меняется на противоположный будем добавлять или удалять пользователя из json файла.

Вначале сохраним флаг в базе при необходимости его изменения а не каждый раз при проверке.

    def set_online(self,value):
        if self.is_online != value:
            self.is_online = value
            self.save()

    def check_online(self):
        if(len(self.sids)>5):
            self.set_online(True)
        else:
            self.set_online(False)

Далее создадим функцию, изменяющую json в отдельном файле utils.py.

    import json
    from imagin.settings import BASE_DIR
    from game.models import Gameuser
    json_path = f'{BASE_DIR}/static/data.json'

    def update_online_users_in_json():
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
        users = []
        for user in Gameuser.objects.filter(is_online=True):
            users.append({'login': user.login, 'image': user.image.url})
            print('append',user.login)
        json_data['users'] = users
        with open(json_path, 'w') as file:
            file.write(json.dumps(json_data))

Тут мы читаем файл с диска и формируем словарь с данными. 

Затем проходим по пользователям в онлайне и заполняем список users.

Потом мы записываем все обратно в файл.

Теперь применим ее в моделе.

    def set_online(self,value):
        if self.is_online != value:
            ...
            from game.utils import update_online_users_in_json
            update_online_users_in_json()

Мы импортируем функцию прямо внутри перед вызовом, чтобы избежать циклического импорта.


### Периодическая отправка json на все веб-сокет соединения.

Создадим отправщик sender.py

    import socketio
    import time
    from datetime import datetime
    from imagin.settings import BASE_DIR
    import json
    json_path = f'{BASE_DIR}/static/data.json'

    mgr = socketio.RedisManager('redis://localhost:6379/0', write_only=True)

    while True:
        time.sleep(2)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with open(json_path,'r') as file:
            json_data = json.loads(file.read())
        mgr.emit('ping', data={'time': current_time,'state': json_data})
        print(current_time)

Тут мы отправляем сообщение в Redis каждые 2 секунды с временной меткой и данными json файла.

Приход сообщения можно отследить в консоле.

![login angular form]({path-to-subject}/images/8.png)


Отработаем событие прихода сообщения ping на клиенте.

        socket.on('ping', msg => {
            console.log(msg);
        })


