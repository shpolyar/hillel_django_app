from django.core.management.base import BaseCommand
import requests
from faker import Faker
from random import uniform
from catalog.models import Category, Goods

URL = 'https://rickandmortyapi.com/api/episode'
fake = Faker()


class Command(BaseCommand):
    help_text = 'Command to fill the database'

    def handle(self, *args, **options):
        req = requests.get(URL)
        # print(req.status_code)
        i = 5  # number of categories
        if req.status_code == 200:
            for item in req.json()['results']:
                if i == 0:
                    break
                else:
                    print(item)
                    category, created = Category.objects.get_or_create(
                        name=item['episode'],
                        description=item['name'],
                        activate=fake.pybool(),
                    )
                    i -= 1
                    for j in range(8):  # number of goods
                        good_url = item['characters'][j]
                        # print(good_url)
                        good_req = requests.get(good_url).json()
                        # print(good_req)
                        if req.status_code == 200:
                            Goods.objects.get_or_create(
                                name=good_req['name'],
                                description=good_req['species'],
                                activate=fake.pybool(),
                                category=category,
                                image=good_req['image'],
                            )
        print('Finish!')
