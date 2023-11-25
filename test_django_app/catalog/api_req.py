import requests

URL = 'http://127.0.0.1:8000/api/category/?format=json'


def get_category():
    req = requests.get(URL)
    print(req.status_code)
    if req.status_code == 200:
        for item in req.json():
            print(item['id'] , item['name'])


get_category()
