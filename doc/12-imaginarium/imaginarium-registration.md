## Регистрация и активация пользователя.

Создадим отдельную модель для пользователей с логином и картинкой.

    class Gameuser(models.Model):
        login = models.CharField(max_length=50,unique=True)
        password = models.CharField(max_length=250,unique=True)
        image = models.ImageField(upload_to='user_images')
        sids = models.TextField(default='')

**login** - уникальный логин, который будем использовать для поиска пользователя.

**sids** - поле с идентификаторами вебсокет соединений в формате списка

    ['blabla1', 'blabla2']

Т.к. пользователь может иметь несколько устройств, подключенных к одной игре.

Производим миграцию.

    ./manage.py makemigrations; ./manage.py migrate

Добавим админку.

    @admin.register(Gameuser)
    class GameuserAdmin(admin.ModelAdmin):
        list_display = ['login', 'sids', 'image']

Создадим класс формы для логина/регистрации в файле forms.py.

    from django.forms import ModelForm
    from game.models import Gameuser

    
    class GameuserForm(ModelForm):
        class Meta:
            model = Gameuser
            fields = ['login', 'password', 'image']

Передадим форму в шаблон главной страницы.


    from game.forms import GameuserForm

    def index(request):
        form = GameuserForm()
        return render(request, 'index.html', {'form': form})

Выведем форму в шаблоне.

    {% extends 'layout.html' %}

    {% block main %}

        <form action="" method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit"> Регистрация/вход </button>
        </form>

    {%  endblock %}


![login angular form]({path-to-subject}/images/2.png)

Отработаем сабмит формы в представлении.

    def index(request):
        if request.method == 'POST':
            form = GameuserForm(request.POST)
            form.save()
        else:
            form = GameuserForm()

        return render(request, 'index.html', {'form': form})

Получаем ошибку валидации.

![login angular form]({path-to-subject}/images/3.png)

Добавим валидацию формы.

        if form.is_valid():
            form.save()

![login angular form]({path-to-subject}/images/4.png)


Сделаем форму способной грузить картинки.

1. Добавим файлы в объект формы

    form = GameuserForm(request.POST, request.FILES)

2. Изменим шаблон и добавим атрибут enctype="multipart/form-data".

    <form action="" method="POST" enctype="multipart/form-data">

Результат.

![login angular form]({path-to-subject}/images/5.png)

Отправим пользователя после регистрации или активации на страницу приветствия.

Для этого вначале создадим функцию поиска пользователя по логину и паролю.

    from game.models import Gameuser

    def find_user(login,password):
        user = None
        try:
            user = Gameuser.objects.get(login=login)
            if user.password == password:
                return user
        except Exception as e:
            print(e)
        return user

Теперь используем поиск в представлении.

    def index(request):
        user = None
        if request.method == 'POST':
            form = GameuserForm(request.POST, request.FILES)
            login = request.POST['login']
            password = request.POST['password']
            user = find_user(login,password)
            if not user:
                if form.is_valid():
                    user = form.save()
        else:
            form = GameuserForm()

        return render(request, 'index.html', {'form': form, 'user': user})

**user = None** - обьявляем пустого пользователя.

**login = request.POST['login']** - забираем логин пользователя из POST.

Можно забирать и из объекта формы так.

    form.cleaned_data['login']

Но при этом мы должны это делать после вызова валидации формы.

    form.is_valid()

Но мы этого сделать не можем т.к. при существовании такого логина получим ошибку валидации формы о том что пользователь с таким логином уже существует.

И такой вариант не проходит.

    def index(request):
        user = None
        if request.method == 'POST':
            form = GameuserForm(request.POST, request.FILES)

            if not user:
                if form.is_valid():
                    user = form.save()
                else:
                    login = form.cleaned_data['login']
                    password = form.cleaned_data['password']
                    user = find_user(login,password)
        else:
            form = GameuserForm()

        return render(request, 'index.html', {'form': form, 'user': user})

Мы получаем ошибку не существования ключа login в form.cleaned_data['login'] т.к. валидация не прошла и в форму не попали очищенные ей данные.

В конце мы добавляем пользователя в шаблон.

Теперь в шаблоне можно проверить на существование пользователя и принять решение о выводе формы.

    {% if user %}
        <h1>Welcome {{ user.login }} !!!</h1>
        <a href="/play">Играть!</a>
    {% else %}
        <form action="" method="POST" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit"> Регистрация/вход </button>
        </form>
    {% endif %}

Осталось решить вопрос с обязательностью картинки.

Предлагаю "не париться" и добавить необязательность **null=True,blank=True** в поле image модели и провести миграцию.

    image = models.ImageField(upload_to='user_images',null=True,blank=True)

![login angular form]({path-to-subject}/images/6.png) 

Теперь добавим логин и картинку пользователя в локальное хранилище браузера 


        <script>
            window.localStorage.setItem('login','{{ user.login }}');
            window.localStorage.setItem('image','{{ user.image.url }}')
        </script>

![login angular form]({path-to-subject}/images/7.png)


Далее будем проверять login на главной в блоке с формой, в случае если он установлен -  перенаправим пользователя на страницу с игрой.

        <script>
            var login = window.localStorage.getItem('login');
            if (login) {
                window.location = '/game';
            } 
        </script>

Полный код шаблона.

    {% extends 'layout.html' %}

    {% block main %}
        {% if user %}
            <h1>Welcome {{ user.login }} !!!</h1>
            <a href="/play">Играть!</a>
            <script>
                window.localStorage.setItem('login','{{ user.login }}');
                window.localStorage.setItem('image','{{ user.image.url }}')
            </script>
        {% else %}
            <form action="" method="POST" enctype="multipart/form-data">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit"> Регистрация/вход </button>
            </form>
            <script>
                var login = window.localStorage.getItem('login');
                if (login) {
                    window.location = '/game';
                } 
            </script>
        {% endif %}
    {%  endblock %}

Создадим роут для страницы с игрой.

    path('game', game, name='game_url'),

Теперь его можно использовать для гибкого создания ссылок по name.

    <a href="{% url 'game_url' %}">Играть!</a> 

Представление.

    def game(request):
        return render(request, 'game.html')



**TODO:** 

1. При вводе неправильного пароля и существующего логина пользователя пускает в систему.

2. Более правильно валидировать форму средствами класса формы а не внутри представления.

3. Неплохо бы задать картинку по дефолту на случай если пользователь ее не загрузил.

4. Вывести кнопку разлогирования в шапке и разлогинить пользователя при нажати очистив локальное хранилище браюзера.


