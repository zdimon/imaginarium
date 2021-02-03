## Рисуем игровую доску.

Создадим 3 поля

    <h2> Игроки </h2>
    <div id="players"></div>
    Игровой стол
    <div id="board"></div>
    У вас на руках
    <div id="hand"></div>

Создадим js функцию для отрисовки игроков в блоке с id = "players".
    

    ...
        socket.on('connect', () => {
            socket.emit('login',{login: window.localStorage.getItem('login')});
            socket.on('ping', msg => {
                draw_users(msg.state)
            })
        });

        var draw_users = function(state) {
            var players_div = $('#players');
            players_div.empty();
            state.users.forEach(function(el){
                players_div.append(`${el.login}:<img width=50 src="${el.image}">`);
            });
        }

    ...


Или более сложная отрисовка по шаблону дизайна.

        var draw_users = function (state) {
            var players_div = $('#players');
                players_div.empty();
                state.users.forEach(function(el){
                    let tpl = `<div class="media align-items-center mb-4">
                               <div class="iq-profile-avatar status-online">
                                  <img class="rounded-circle avatar-50" src="${el.image}" alt="">
                               </div>
                               <div class="media-body ml-3">
                                  <h6 class="mb-0"><a href="#">Anna Sthesia</a></h6>
                                  <p class="mb-0">${el.login}</p>
                               </div>
                            </div>`
                    players_div.append(tpl);
                });        
        }

Для того, чтобы мы увидели изображения из папки media добавим роут в urls.py.

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Создадим js функцию для отрисовки карт на столе в блоке с id = "board".


        socket.on('connect', () => {
            socket.emit('login',{login: window.localStorage.getItem('login')});
            socket.on('ping', msg => {
                draw_users(msg.state);
                draw_board(msg.state);
            })
        });

        ....

        var draw_board = function(state) {
            var board_div = $('#board');
            board_div.empty();
            state.table.forEach(function(el){
                board_div.append(`<img width=50 src="${el.image}">`);
            });
        }

Создадим js функцию для отрисовки карт на руках в блоке с id = "hand".

    socket.on('connect', () => {
            socket.emit('login',{login: window.localStorage.getItem('login')});
            socket.on('ping', msg => {
                ....
                draw_hand(msg.state);
            })
        });

      ...

        var draw_hand = function(state) {
            var hand_div = $('#hand');
            hand_div.empty();
            var user_login = window.localStorage.getItem('login');
            state.users.forEach(function(el){
                if(el.login === user_login) {
                    el.cards.forEach(function(card){
                        hand_div.append(`<img width=50 src="${card.image}">`);
                    })
                }
                
            });
        }

Добавим несколько карт каждому пользователю для тестов в utils.py.
    
    ....
    def update_online_users_in_json():
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
        users = []
        for user in Gameuser.objects.filter(is_online=True):
            users.append({ \
                 'login': user.login, \
                 'image': user.image.url, \
                 'cards': [ \
                     {'image': 'static/images/cards/8.jpg'}, \
                     {'image': 'static/images/cards/9.jpg'}, \
                 ]}) 
     ....

Результат.

![login angular form]({path-to-subject}/images/9.png)





