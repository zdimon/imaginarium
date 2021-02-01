from game.models import Gameuser
from imagin.settings import BASE_DIR
json_path = f'{BASE_DIR}/static/data.json'
import json

def find_user(login,password):
    user = None
    try:
        user = Gameuser.objects.get(login=login)
        if user.password == password:
            return user
    except Exception as e:
        print(e)
    return user


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
                 ]
             }) 
    print('append',user.login)
    json_data['users'] = users
    with open(json_path, 'w') as file:
        file.write(json.dumps(json_data))        








