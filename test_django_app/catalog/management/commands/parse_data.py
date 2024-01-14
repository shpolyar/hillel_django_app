from urllib.parse import urljoin

import requests
from django.core.management.base import BaseCommand
from catalog.models import Category, Goods
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.defaultfilters import slugify
from transliterate import translit
import datetime

# URL = 'https://rozetka.com.ua/mobile-phones/c80003/producer=apple/'
URL = 'https://ukrzoloto.ua'


class Command(BaseCommand):
    help_text = 'Parse data'

    @staticmethod
    def translit_word(name):
        return translit(name, 'ru', reversed=True)

    @staticmethod
    def download_image(good_img_url, image_name):
        image_src = f'{settings.BASE_DIR}/media/image/{image_name}.jpg'
        img_data = requests.get(good_img_url).content
        with open(image_src, 'wb') as handler:
            handler.write(img_data)
        return f'image/{image_name}.jpg'

    def handle(self, *args, **options):
        start_time = datetime.datetime.now()
        print('Start!')
        r = requests.get(URL + '/catalog')
        bs = BeautifulSoup(r.content, 'html5lib')
        for category_num, item in enumerate(bs.find_all("a", {"class": "catalogue-categories__link"})):
            if category_num == 5:
                break
            name = item.get_text()
            activate = True
            url = urljoin(URL, item.get('href'))
            category, created = Category.objects.get_or_create(
                name=name,
                activate=activate,
                description=url,
            )
            r1 = requests.get(url)
            bs1 = BeautifulSoup(r1.content, 'html5lib')
            for good_num, good in enumerate(bs1.find_all("div", {"class": "product-card__content"})):
                if good_num == 10:
                    break
                good_name = good.select_one('.title').get_text()
                good_img_url = good.select_one('.image').get('src')
                good_price = good.select_one('.price__current span').get_text().replace(' ', '')
                Goods.objects.get_or_create(
                    name=f'{good_name}_{good_num}',
                    description=self.translit_word(good_name),
                    price=good_price,
                    activate=True,
                    category=category,
                    image=self.download_image(good_img_url, slugify(self.translit_word(good_name))),
                )
        print('Success!')
        print('Used time:', datetime.datetime.now() - start_time)
