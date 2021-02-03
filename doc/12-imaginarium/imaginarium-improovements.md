# Улучшения

Делаем функцию очистки стола и сброса всех игроков в статус 'beter'.

    def clear_table():
        with open(json_path, 'r') as file:
            json_data = json.loads(file.read())
        json_data['table'] = []
        with open(json_path, 'w') as file:
            file.write(json.dumps(json_data)) 
        for c2u in Card2User.objects.filter(position='table'):
            c2u.delete()
        for user in Gameuser.objects.filter():
            user.state = 'betor'
            user.save()
            dial_cards_to_user(user)

Очищаем стол при логине

    def index(request):
        user = None
        if request.method == 'POST':
           ...
            clear_table()

Добавим функцию поиска загадывающего.

        get_gessor = function(users){
            for(var i=0; i<=users.length-1; i++) {
                if (users[i].state === 'gessor' || 'gessed') 
                {
                    return users[i];
                }
            }
        }

Применим ее при перерисовке пользователей.

            var gessor = get_gessor(state.users);
            if(gessor) {
                var gessor_image = $('#gessor_image');
                let tpl = `<img src="${gessor.image}" alt="avatar" class="avatar-50 ">
                <span class="avatar-status"><i class="ri-checkbox-blank-circle-fill text-success"></i></span>`;
                gessor_image.empty();
                gessor_image.append(tpl);
            }  

Создадим команду очистки пользователей.

    from django.core.management.base import BaseCommand, CommandError
    from game.models import Gameuser
    from django.core.files import File
    from imagin.settings import BASE_DIR

    class Command(BaseCommand):
        
        def handle(self, *args, **options):
            print('clear users')
            Gameuser.objects.all().delete()

## Определение браузерного хранилища.

Определим глобальную переменную в .env.

    BROWSER_STORAGE='sessionStorage'

Возмем ее в настройках.

    from dotenv import load_dotenv
    load_dotenv()
    ...
    BROWSER_STORAGE = os.getenv('BROWSER_STORAGE','sessionStorage')

Прокинем в шаблон.

    from imagin.settings import BROWSER_STORAGE

    def index(request):
        ....
        
        return render(request, 'index.html', {... "storage": BROWSER_STORAGE})

Используем в шаблоне.


        <script>
            var login = window.{{storage}}.getItem('login');
            if (login) {
                window.location = '/game';
            } 
        </script>

## Разлогирование 

Шаблон

    <h1>Good buy !!!</h1>
     <script>
        window.{{storage}}.removeItem('login');
        window.{{storage}}.removeItem('image');
        window.location = '/';
     </script>

Представление.

    from django.shortcuts import render
    from game.models import Gameuser
    from imagin.settings import BROWSER_STORAGE

    def logout(request,login):
        user = Gameuser.objects.get(login=login)
        user.delete()
        return render(request, 'logout.html',{"storage": BROWSER_STORAGE})

