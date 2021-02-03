# Создаем непрерывную интеграцию через GIT.
      
Создадим скрипт деплоя imagin/deploy.

    cd ..
    . ./venv/bin/activate
    git pull
    pip install -r requirements.txt
    cd imagin
    ./manage.py migrate

Добавим право его исполнять.

    chmod +x ./imagin/deploy

Создадим отображение для запуска скрипта деплоя.

    from django.http import HttpResponse
    import subprocess
    from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def deploy(request):
        rc = subprocess.call("./deploy", shell=True)
        return HttpResponse('Ok') 


Добавим роутинг.

    path('deploy', deploy),

Добавим хук на github.

![login angular form]({path-to-subject}/images/12.png)

![login angular form]({path-to-subject}/images/13.png)

## Добавление названия текущей ветки на все страницы.

Установим библиотеку pygit2

    pip install GitPython

Создадим файл текстового процессора imagin/git_processor.py

    from git import Repo

    def get_current_branch(request):
        local_repo = Repo(path='../')
        local_branch = local_repo.active_branch.name       
        return {'git_branch': local_branch}

Добавим процессор в настройки.

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'imagin.git_processor.get_current_branch', \
                ],
            },
        },
    ]

Выведем в шаблоне.

    branch ({{ git_branch }})


