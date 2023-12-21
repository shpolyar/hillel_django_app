import requests

# URL = 'https://rickandmortyapi.com/api/location'
URL = 'https://api-seller.rozetka.com.ua/sites'

def get_category():
    req = requests.get(URL)
    print(req.status_code)
    if req.status_code == 200:
        for item in req.json()['results']:
            print(item)

get_category()
# req = requests.get(URL)
# print(req.status_code)
# print(req.json())
