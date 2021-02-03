from game.models import Gameuser, Card2User, Card
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
             'state': user.state, \
             'association': user.association, \
             'cards': [
                 { \
                    'id':item.card.id, \
                    'image':item.card.image.url, \
                 } for item in Card2User.objects.filter(user=user, position='hand')
             ]
             }) 
        print('append',user.login)
    json_data['users'] = users
    with open(json_path, 'w') as file:
        file.write(json.dumps(json_data))        


def get_random_card():
    return Card.objects.all().order_by('?').first()
    #return Card.objects.filter(on_hand=False).order_by('?').first()

def put_user_cards_to_json(user):
    with open(json_path, 'r') as file:
        json_data = json.loads(file.read())
        
    cards = [{ \
        'id':item.card.id, \
        'image':item.card.image.url, \
        } for item in Card2User.objects.filter(user=user,position='hand')]
    for u in json_data['users']:
        if u['login'] == user.login:
            u['cards'] = cards

    with open(json_path, 'w') as file:
        file.write(json.dumps(json_data))

def dial_cards_to_user(user):
    count_cards = Card2User.objects.filter(user=user,position='hand').count()
    for number in range(count_cards,6):
        card = get_random_card()
        c2u = Card2User()
        c2u.user = user
        c2u.card = card
        c2u.save()
        card.on_hand = True
        card.save()
    put_user_cards_to_json(user)


def put_card_on_table_json(user,card,is_right):
    c2u = Card2User.objects.get(user=user,card=card,position='hand')
    c2u.position = 'table'
    c2u.is_right = is_right
    c2u.save()
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
