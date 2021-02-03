# Контролируем статус игроков.
     
Определим в каких состояниях может находится игрок для того, чтобы соответственно изменять его интерфейс и позволять делать то, что позволяет его состояние.

gessor - тот кто загадывает изображение и ассоциацию (доступно выбор карты и фразы)

gessed - после того как загадал (становится недоступным выбор карты)

betor - тот кто ставит карту и угадывает ассоциацию (доступно выбор карты)

beted - после того как поставил карту (становится недоступным выбор карты)

proposer - кто отгадывает

proposed - кто отгадал

Введем новое поле в модель игроков и применим миграцию.

    USER_STATES = (
        ("gessor", "gessor"),
        ("gessed", "gessed"),
        ("betor", "betor"),
        ("beted", "beted"),
        ("proposer", "proposer"),
        ("proposed", "proposed")
    )

    class Gameuser(models.Model):
        ...
        state = models.CharField(max_length=10,
                            choices=USER_STATES,
                            default="betor")

Добавим поле в функции update_online_users_in_json.

    def update_online_users_in_json():
        ...
        for user in Gameuser.objects.filter(is_online=True):
            users.append({ \
                 'login': user.login, \
                 'state': user.state, \
                 ....

Выведем кнопку старта игры в случае, если все пользователи имеют статус better и кто первый на нее нажмет, станет gessor.

Шаблон.

       <div id="start_button" style="display: none">
          <button type="submit" class="btn btn-primary d-flex align-items-center p-2"><i class="fa fa-paper-plane-o" aria-hidden="true"></i><span class="d-none d-lg-block ml-1">Start the game</span></button>
       </div>


Обьявим такую функцию.

        var draw_start_button = function(state) {
            var is_show = true;
            var hand_div = $('#start_button');
            state.users.forEach(function(el){
                if(el.state === 'gessor') {
                    is_show = false;
                }
            });
            if(is_show === true) {
                
                hand_div.show();
                $('#start_button').on('click',function() {
                    $.ajax('/start', {
                                data : JSON.stringify({
                                    login: window.localStorage.getItem('login')
                                    }),
                                contentType : 'application/json',
                                type : 'POST',
                                success: function(data) {
                                    console.log(data);
                                }
                            });                    
                })
            }  else {
                hand_div.hide();
            }
        }

Задействуем при событии прихода сообщения о состоянии игры.


        socket.on('connect', () => {
            socket.emit('login',{login: window.localStorage.getItem('login')});
            socket.on('ping', msg => {
                console.log(msg);
                draw_users(msg.state);
                draw_board(msg.state);
                draw_hand(msg.state);
                draw_start_button(msg.state);
            })
        });

 
Создадим роут.

    path('start/game', start_game),

Создадим представление.

    @csrf_exempt
    def start_game(request):
        data = json.loads(request.body)
        user = Gameuser.objects.get(login=data['login'])
        user.state = 'gessor'
        user.save()
        update_online_users_in_json()
        return HttpResponse('OK')

Подкрасим индикатор на аватарке в зависимости от состояния пользователя.

        if(el.state === 'gessor'){
            var status = 'online';
        } else {
            var status = 'offline';
        }
        let tpl = `<div class="media align-items-center mb-4">
                   <div class="iq-profile-avatar status-${status}">

        ....

Теперь нам необходимо на фронтенде определить функцию поиска текущего пользователя для того, чтобы дальше по его состоянию скрывать или отображать те или иные блоки.

        get_current_user = function(users){
            for(var i=0; i<=users.length-1; i++) {
                if (users[i].login === window.localStorage.getItem('login')) 
                {
                    console.log(users[i]);
                    return users[i];
                }
            }
        }

И использовать ее для показа или скрытия блока.

        var draw_help_message = function(state) {
            var block = $('#help_message');
            var user = get_current_user(state.users);
            if(user.state === 'gessor') {
                var message = 'Загадывайте ассоциацию и выбирайте картинку!';
               
            } else if(user.state === 'gessed') {
                var message = 'Подождите пока все игроки попытаются угадать.';
               
            } else if(user.state === 'betor') {
                var message = 'Подождите пока загадают ассоциацию и выберете под нее картинку.';
               
            } else if(user.state === 'beted') {
                var message = 'Подождите пока все игроки выложат по картинке.';
               
            } else if(user.state === 'proposer') {
                var message = 'Пробуйте угадать правильную картинку.';
               
            } else if(user.state === 'proposeed') {
                var message = 'Ожидайте пока все не сделают ставки.';
               
            }
            else {
                var message = 'Сообщения нет!';
            }
            block.empty();
            block.html(message);
            
        }

Теперь, когда мы имеем состояние игрока мы можем это использовать для запуска разных обработчиков при клике на изображения.


Например так.

        var user = get_current_user(state.users);
        if(user.state === 'gessor') {
            $(`#user-card-${card.id}`).on('click', function(el) {
                alert('gessing');
            });
        }
        if(user.state === 'betor') {
            $(`#user-card-${card.id}`).on('click', function(el) {
                alert('betting');
            });
        }

И послать данные на разные урлы.

        var obj = $(el.target);
        var data = {
                    login: window.localStorage.getItem('login'),
                    card_id: obj.attr('data-card-id')
                }
        var user = get_current_user(state.users);
        if(user.state === 'gessor') {
            $(`#user-card-${card.id}`).on('click', function(el) {

                $.ajax('/make/gess', {
                    data : JSON.stringify(data),
                    contentType : 'application/json',
                    type : 'POST',
                    success: function(data) {
                        console.log(data);
                    }
                });

            });
        }
        if(user.state === 'betor') {
            $(`#user-card-${card.id}`).on('click', function(el) {
                $.ajax('/make/bet', {
                    data : JSON.stringify(data),
                    contentType : 'application/json',
                    type : 'POST',
                    success: function(data) {
                        console.log(data);
                    }
                });
            });
        }

Переопределим метод save в модели пользователя и будем обновлять всех пользователей в онлайне при изменении одного из них.

    class Gameuser(models.Model):
       ...
        def save(self, *args, **kwargs):
            from game.utils import update_online_users_in_json
            super(Gameuser, self).save(*args, **kwargs)
            update_online_users_in_json()




Осталось подсчитать очки пользователей.

Добавим поле в модель.

    class Gameuser(models.Model):
      ...
        account = models.IntegerField(default=0)

Создадим команду для очистки данных чтобы легче возвращаться в исходное состояние при тестировании.

    from django.core.management.base import BaseCommand, CommandError
    from game.models import Card2User, Gameuser, Card
    from django.core.files import File
    from imagin.settings import BASE_DIR
    json_path = f'{BASE_DIR}/static/data.json'
    json_tpl = '{"table": [], "users": [], "status": "start", "association": ""}'

    class Command(BaseCommand):
        
        def handle(self, *args, **options):
            print('Clear data')

            print('Clear data')
            Card2User.objects.all().delete()
            for u in Gameuser.objects.all():
                u.state = 'bettor'
                u.save()
            for c in Card.objects.all():
                c.on_hand = False
                c.save()
            with open(json_path, 'w') as file:
                file.write(json_tpl)


