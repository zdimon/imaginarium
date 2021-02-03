## Функция загадывания ассоциации.

Реализуем на фронтенде передачу содержимого поля куда игрок вводит текст ассоциации на бекенд.

Добавим id элементу input

    <input ... id="assoc-input">

Подмешаем значение в отправляемый json.

        var myJSObject = {
            ...
            assoc: $('#assoc-input').val()
        };

Добавим поле к пользователю с текстом ассоциации.

    class Gameuser(models.Model):
        ...
        association = models.TextField(default="empty")

Подмешаем ассоциацию в json.

    def update_online_users_in_json():
        ...
        for user in Gameuser.objects.filter(is_online=True):
            users.append({ \
                 '...
                 'association': user.association, \

Выведем ее в шаблоне.

    <h5 class="mb-0" id="association_text">No assotiation</h5>

    ...

    if(gessor) {
                ...
                $('#association_text').html(gessor.association);
            }

Сохраним ассоциацию в базе при запросе.

    @csrf_exempt
    def gessing(request):
        data = json.loads(request.body)
        user = Gameuser.objects.get(login=data['login'])
        user.state = 'gessed'
        user.association = data['assoc'] 
        ...

Решим задачу с перевернутыми картами.

Добавим поле в модель и проведем миграцию.

    class Card2User(models.Model):
        ...
        is_down = models.BooleanField(default=False)

Отметим влаг в запросе на загадывание карты в utils.py. 

    def put_card_on_table_json(user,card,is_right):
        c2u = Card2User.objects.get(user=user,card=card,position='hand')
        c2u.position = 'table'
        c2u.is_right = is_right
        c2u.is_down = True;

    ...

Изменим логику отображения картинок.

        if(el.is_down) {
            var imgurl = '/static/images/back.png';
        } else {
            var imgurl = el.image;
        }
        board_div.append(`<img data-card-id="${el.id}" id="${el.id}-board-card" src="${imgurl}">`);

Перевернем картинки в случае когда все игроки выложили по карте.

    def put_card_on_table_json(user,card,is_right):
        c2u = Card2User.objects.get(user=user,card=card,position='hand')
        c2u.position = 'table'
        c2u.is_right = is_right
        c2u.is_down = True;
        c2u.save()
        ## Переворачиваем
        if not is_right:
            count_cards = Card2User.objects.filter(position='table').count()
            count_users = Gameuser.objects.filter(is_online=True).count()
            if count_cards == count_users:
                for c in Card2User.objects.filter(position='table'):
                    c.is_down = False
                    c.save()
                    
        ###
        card.on_hand = False
        card.save()
        
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
        ## Тут берем из базы
        table = [ 
            { 
                "id": item.card.id, 
                "image": item.card.image.url, 
                "is_down": item.is_down, 
                "is_true": item.is_right                 
            } 
            for item in Card2User.objects.filter(position='table') 
        ]
        json_data['table'] = table
        with open(json_path, 'w') as file:
            file.write(json.dumps(json_data))
        put_user_cards_to_json(user)





