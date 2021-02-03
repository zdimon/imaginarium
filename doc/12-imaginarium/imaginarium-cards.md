## Раздаем карты.

Создадим модель под список карт и проведем миграцию.

    class Cards(models.Model):
        on_hand = models.BooleanField(default=False)
        image = models.ImageField(upload_to='user_images',null=True,blank=True)     

on_hand - признак того, что карта роздана

Админка.

    @admin.register(Card)
    class CardAdmin(admin.ModelAdmin):
        list_display = ['image', 'on_hand']

В моделе можно создадть специальную функцию для вывода тега картинки.


    from django.utils.safestring import mark_safe


    class Card(models.Model):
        on_hand = models.BooleanField(default=False)
        image = models.ImageField(upload_to='user_images',null=True,blank=True)

        def image_tag(self):
            return mark_safe(f'<img src="{self.image.url}" width=100 />')

И добавить его в админку.

    @admin.register(Card)
    class CardAdmin(admin.ModelAdmin):
        list_display = ['image_tag', 'on_hand']

Создадим команду для загрузки карт в базу.

    from django.core.management.base import BaseCommand, CommandError
    from game.models import Card
    from django.core.files import File
    from imagin.settings import BASE_DIR

    class Command(BaseCommand):
        
        def handle(self, *args, **options):
            print('Load cards')
            Card.objects.all().delete()
            for i in range(1,19):
                card = Card()
                card.save()
                filepath = f'{BASE_DIR}/static/images/{i}.jpg'
                with open(filepath, 'rb') as doc_file:
                    card.image.save(f'{i}.jpg', File(doc_file), save=True)
                print(f'Creating card {i}')

Создадим модель для привязки выданных карт пользователям и проведем миграцию.

    class Card2User(models.Model):
        user = models.ForeignKey(Gameuser,on_delete=models.CASCADE)
        card = models.ForeignKey(Card,on_delete=models.CASCADE)

Создадим функции для раздачи карт пользователям не больше 6 на руки.

    def get_random_card():
        return Card.objects.filter(on_hand=False).order_by('?').first()

    def dial_cards_to_user(user):
        count_cards = Card2User.objects.filter(user=user).count()
        for number in range(count_cards,6):
            card = get_random_card()
            c2u = Card2User()
            c2u.user = user
            c2u.card = card
            c2u.save()
            card.on_hand = True
            card.save()

Протестируем в отображении.


    from game.models import Gameuser
    from game.utils import dial_cards_to_user
    ...
    def game(request):
        for u in Gameuser.objects.filter(is_online=True):
            dial_cards_to_user(u)
        return render(request, 'game.html')

Создадим функцию сохранения карт, которые на руках пользователя в json.

    def put_user_cards_to_json(user):
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
            
        cards = [{ \
            'id':item.card.id, \
            'image':item.card.image.url, \
            } for item in Card2User.objects.filter(user=user)]
        for u in json_data['users']:
            if u['login'] == user.login:
                u['cards'] = cards

        with open(json_path, 'w') as file:
            file.write(json.dumps(json_data))

И используем ее.

    def dial_cards_to_user(user):

        ....

        put_user_cards_to_json(user)

После чего уберем хардкод из 

    def update_online_users_in_json():
       ....
        for user in Gameuser.objects.filter(is_online=True):
            users.append({ \
                 'login': user.login, \
                 'image': user.image.url, \
                 'cards': [ \
                         {'image': 'static/images/cards/8.jpg'}, \
                         {'image': 'static/images/cards/9.jpg'}, \
                     ]
                 }) 

И добавим выборку карт из БД.

        users.append({ \
             'login': user.login, \
             'image': user.image.url, \
             'cards': [
                 { \
                    'id':item.card.id, \
                    'image':item.card.image.url, \
                 } for item in Card2User.objects.filter(user=user)
             ]
             }) 

![login angular form]({path-to-subject}/images/14.png)






