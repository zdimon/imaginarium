## Функция разгадывания ассоциации.

Подвяжем функцию обратного вызова на карты что на столе для пользователя со статусом beted.

                var user = get_current_user(state.users);
                if(user.state === 'beted') {
                    $(`#${el.id}-board-card`).addClass('pointer');
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
                }

Выделим карту для пользователя со статусом proposed и уберем событие клика.

                if(user.state === 'proposed') {
                    $(`#${el.id}-board-card`).addClass('checked');
                    $(`#${el.id}-board-card`).off('click');
                }

Добавим поле с аккаунтом в модель пользователей.

    class Gameuser(models.Model):
       ...
        account = models.IntegerField(default=0)

Добавим поле в json.

    def update_online_users_in_json():
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
        users = []
        for user in Gameuser.objects.filter(is_online=True):
            users.append({ \
                 'login': user.login, \
                 'image': user.image.url, \
                 'state': user.state, \
                 'account': user.account, \

        ....

Переопределим функцию delete у модели Card2User и сбросим флаг, который говорит что она на руках.

    class Card2User(models.Model):
        ...
        def delete(self, *args, **kwargs):
            card = self.card
            card.on_hand = False
            card.save()
            super(Gameuser, self).save(*args, **kwargs)


Создадим функцию подсчета очков если не осталось пользователей со статусом propose, bet и beted.

    def try_to_count():
        usercheck = Gameuser.objects.filter(Q(state='propose') | Q(state='bet') | Q(state='beted'), is_online=True).count()
        print('Checkuser ', usercheck)
        if usercheck == 0:
            for p in Propose.objects.all():
                if p.is_right:
                    user = p.proposer
                    user.account += 1
                    user.save()

            Card2User.objects.filter(position='table').delete()
            for user in Gameuser.objects.filter(is_online=True):
                dial_cards_to_user(user)










