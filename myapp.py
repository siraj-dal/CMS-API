import requests
import json

url = "http://127.0.0.1:8000/cms_api_data/"

param = {
        'type': 'user'
    }
post_type = 'public'

def get_data(user_id=None):
    data = {}
    if id:
        data = {'user_id' : user_id,
                }
    json_data = json.dumps(data)
    print(json_data)
    r = requests.get(url=url, data=json_data, params=param)
    data = r.json()
    print(data)

# get_data()


def post_data():
    if param.get('type') == 'user':

        data = {
            'user_id': 'A001',
            'name': 'Ashad',
            'email': 'Asd@gmail.com',
            'password': '45645645',
        }

    else:
        data = {
            'post_id' : 'P001',
            'user_id': 'S121',
            'title': 'REST APIs: How They Work and What You Need to Know',
            'description': 'In the interconnected world of software applications, sharing data between systems has become the cornerstone of functionality and service diversity. One key player that has revolutionized this data sharing and communication is REST APIs, acting as the enabler for integrations.',
            'content': 'quotes',
            'post_type': post_type
        }

    json_data = json.dumps(data)
    print(json_data)
    r = requests.post(url=url, data=json_data, params=param)
    data = r.json()
    print(data)


post_data()


def update_data():
    data = {
        'id' : 7,
        'user_id': 'A222',
        'name': 'Ashad Khira',
        'email':'ashad@gmail.com',
        'password':'45878555'
    }
    json_data = json.dumps(data)
    print(json_data)
    r = requests.put(url=url, data=json_data, params=param)
    data = r.json()
    print(data)


# update_data()


def delete_data():
    data = {'id': 10}
    json_data = json.dumps(data)
    print(json_data)
    r = requests.delete(url=url, data=json_data, params=param)
    data = r.json()
    print(data)


# delete_data()