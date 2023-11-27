import requests

URL = 'https://rickandmortyapi.com/api/location'


def get_category():
    req = requests.get(URL)
    print(req.status_code)
    if req.status_code == 200:
        for item in req.json()['results']:
            print(item['id'], item['name'])
            print('*'*30)
            print(item['residents'])


get_category()
