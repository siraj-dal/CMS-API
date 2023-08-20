import requests
import json

# url = "http://127.0.0.1:8000/cms_api_data/"
# data = {
#     'user_id':'V001',
#     'name':'Vivek',
#     'email':'VG@gmail.com',
#     'password':'12452525',
# }
# json_data = json.dumps(data)
# print(json_data)
# r = requests.post(url=url,data=json_data)
# data = r.json()
# print(data)

url = "http://127.0.0.1:8000/cms_api_data/"

def get_data(id=None):
    data = {}
    if id is not None:
        data = {'id' : id}
    json_data = json.dumps(data)
    print(json_data)
    r = requests.get(url=url, data=json_data)
    data = r.json()
    print(data)

get_data()
