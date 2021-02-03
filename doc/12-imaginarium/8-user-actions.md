# Действия пользователя.

В игре будет 3 типа действия.

1. Загадывание карты и ассоциации

2. Выкладывание карты под загаданную ассоциацию

3. Угадывание правильной карты.

Все эти запросы будут присходить в фоновом режиме браузера AJAX запросами. 

Поэтому они носят название API.

## Реализуем загадывание карты и выкладывание и пользователем на стол.

Для этого создадим отображение в файле views/api/gessing.py с роутингом.

    from django.views.decorators.csrf import csrf_exempt
    from django.http import HttpResponse

    @csrf_exempt
    def gessing(request):
        return HttpResponse('OK')

Роутинг.

    path('gessing', gessing),

В шаблоне добавим обработчик к каждой карте  по id.

        el.cards.forEach(function(card){
            hand_div.append(`
            <img width=50 src="${card.image}">
            <button  data-card-id="${card.id}" id="${card.id}-btn">V</button>
            `);
            $(`#${card.id}-btn`).on('click', function(el) {
                console.log(el);
            });
        
        })

Теперь в обработчике передадим данные (логин и id карты) POST запросом.

        var obj = $(el.target);

        var myJSObject = {
            login: window.localStorage.getItem('login'),
            card_id: obj.attr('data-card-id')
        };

        $.ajax('/gessing', {
            data : JSON.stringify(myJSObject),
            contentType : 'application/json',
            type : 'POST',
            success: function(data) {
                console.log(data);
            }
        });

В отображении получить пришедшие данные и преобразовать их в словарь можно так:

    data = json.loads(request.body)

Создадим вспомогательную функцию, выкладывающую одну карту в json.

    def put_card_on_table_json(user,card):
        c2u = Card2User.objects.get(user=user,card=card)
        c2u.delete()
        card.on_hand = False
        card.save()
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
        json_data['table'].append( \
            { \
                "id": card.id, \
                "image": card.image.url, \
                "is_true": "false" \
            } \
        ) 
        with open(json_path, 'w') as file:
            file.write(json.dumps(json_data))
        put_user_cards_to_json(user)


Задейсвуем во вьюхе.


    import json
    from game.models import Card, Gameuser
    ...

    @csrf_exempt
    def gessing(request):
        data = json.loads(request.body)
        user = Gameuser.objects.get(login=data['login'])
        card = Card.objects.get(pk=data['card_id'])
        put_card_on_table_json(user,card)
        return HttpResponse('OK')

![login angular form]({path-to-subject}/images/15.png)

Теперь необходимо решить такую проблему.

Необходимо запретить пользователю выкладывать более 1 карты на стол.

Надежней это сделать на стороне бекенда и выдать предупреждение в случае такой попытки.

Создадим дополнительное поле position в модели Card2User в котором будем отмечать где именно находится карта пользователя.


    POSITION = (
        ("hand", "hand"),
        ("table", "table")
    )

    class Card2User(models.Model):
        user = models.ForeignKey(Gameuser,on_delete=models.CASCADE)
        card = models.ForeignKey(Card,on_delete=models.CASCADE)
        position = models.CharField(max_length=10,
                            choices=POSITION,
                            default="betor")

Теперь подправим функцию dial_cards_to_user c учетом этого поля.

    def dial_cards_to_user(user):
        count_cards = Card2User.objects.filter(user=user,position='hand').count()

Так же его необходимо учесть и при выводе карт на руках.

    def put_user_cards_to_json(user):
         ....
            
        cards = [{ \
            'id':item.card.id, \
            'image':item.card.image.url, \
            } for item in Card2User.objects.filter(user=user,position='hand')]


Выведем его в админке.

    @admin.register(Card2User)
    class Card2UserAdmin(admin.ModelAdmin):
        list_display = ['user', 'card', 'position']

Переведем позицию в запросе gessing и проверим на дубликат.

    @csrf_exempt
    def gessing(request):
        data = json.loads(request.body)
        user = Gameuser.objects.get(login=data['login'])
        card = Card.objects.get(pk=int(data['card_id']))
        try:
            Card2User.objects.get(user=user,position='table')
            return HttpResponse('Error')
        except Exception as e:
            put_card_on_table_json(user,card)
            return HttpResponse('OK')


Card2User.objects.get(user=user,position='table') - тут мы проверяем есть ли у пользователя одна карта на столе.

Теперь добавим в модель поле is_right по которому будем определять какая карта правильная из тех что на столе.

    class Card2User(models.Model):
        ....
        is_right = models.BooleanField(default=False)

Потом добавим дополнительный параметр

    put_card_on_table_json(user,card, True)

И отметим карту в функции put_card_on_table_json

    def put_card_on_table_json(user,card,is_right):
        c2u = Card2User.objects.get(user=user,card=card,position='hand')
        c2u.position = 'table'
        c2u.is_right = is_right
        ...

Аналогично сделаем запрос на выкладывание карты под загаданную ассоциацию (betting).

Только выставим флаг is_right в false.

    from django.views.decorators.csrf import csrf_exempt
    from django.http import HttpResponse
    import json
    from game.utils import put_card_on_table_json
    from game.models import Gameuser, Card, Card2User

    @csrf_exempt
    def betting(request):
        data = json.loads(request.body)
        user = Gameuser.objects.get(login=data['login'])
        card = Card.objects.get(pk=int(data['card_id']))
        try:
            Card2User.objects.get(user=user,position='table')
            return HttpResponse('Error')
        except Exception as e:
            put_card_on_table_json(user,card, False)
            return HttpResponse('OK')

Наконец для того, чтобы реализовать последний запрос, когда игроки угадывают правильную карту нам понадобиться еще одна модель.

    class Propose(models.Model):
        proposer = models.ForeignKey(Gameuser,on_delete=models.CASCADE,related_name='proposer')
        owner = models.ForeignKey(Gameuser,on_delete=models.CASCADE,related_name='owner')
        card = models.ForeignKey(Card,on_delete=models.CASCADE)

Админка.

    @admin.register(Propose)
    class ProposeAdmin(admin.ModelAdmin):
        list_display = ['owner', 'proposer', 'card', 'is_right']

Создаем роут под запрос.

    path('propose', propose),

Отображение.

    from django.views.decorators.csrf import csrf_exempt
    from django.http import HttpResponse
    from game.models import Gameuser, Card, Card2User, Propose
    import json

    @csrf_exempt
    def propose(request):
        data = json.loads(request.body)
        user = Gameuser.objects.get(login=data['login'])
        card = Card.objects.get(pk=int(data['card_id']))
        c2u = Card2User.objects.get(card=card,position='table')
        try:
            p = Propose.objects.get(proposer=user)
            return HttpResponse('Error')
        except:
            p = Propose()
            p.owner = c2u.user
            p.proposer = user
            p.card = card
            if c2u.is_right:
                p.is_right = True
            p.save()
        return HttpResponse('OK')
    
Фронтенд. Привязываем событие клика на карту на столе в шаблоне.

        var draw_board = function(state) {
                var board_div = $('#board');
                board_div.empty();
                state.table.forEach(function(el){
                    board_div.append(`<img data-card-id="${el.id}" id="${el.id}-board-card" src="${el.image}">`);

                    $(`#${el.id}-board-card`).on('click', function(el) {
                        var obj = $(el.target);
                        var myJSObject = {
                            login: window.localStorage.getItem('login'),
                            card_id: obj.attr('data-card-id')
                        };
                        $.ajax('/propose', {
                            data : JSON.stringify(myJSObject),
                            contentType : 'application/json',
                            type : 'POST',
                            success: function(data) {
                                console.log(data);
                            }
                        });
                    });
                    
                });
            };





