from urllib.parse import urljoin
from models import Category, Goods
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.defaultfilters import slugify
from transliterate import translit
import datetime
import asyncio
import aiohttp
import aiofiles
from django.core.management.base import BaseCommand

URL = 'https://ukrzoloto.ua'


async def req_body(url):
    async with aiohttp.ClientSession as session:
        async with session.get(url) as resp:
            body = await resp.text()
            return body


def translit_word(name):
    return translit(name, 'ru', reversed=True)


async def download_image(good_img_url, image_name):
    async with aiohttp.ClientSession as session:
        async with session.get(good_img_url) as resp:
            img_data = await resp.read()
    image_src = f'{settings.BASE_DIR}/media/image/{image_name}.jpg'
    async with aiofiles.open(image_src, 'wb') as handler:
        await handler.write(img_data)
    return f'image/{image_name}.jpg'


async def parse():
    start_time = datetime.datetime.now()
    print('Start!')
    content = await req_body(URL + '/catalog')
    bs = BeautifulSoup(content, 'html5lib')
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
        good_content = await req_body(url)
        bs1 = BeautifulSoup(good_content, 'html5lib')
        for good_num, good in enumerate(bs1.find_all("div", {"class": "product-card__content"})):
            if good_num == 10:
                break
            good_name = good.select_one('.title').get_text()
            good_img_url = good.select_one('.image').get('src')
            good_price = good.select_one('.price__current span').get_text().replace(' ', '')
            Goods.objects.get_or_create(
                name=f'{good_name}_{good_num}',
                description=translit_word(good_name),
                price=good_price,
                activate=True,
                category=category,
                image=download_image(good_img_url, slugify(translit_word(good_name))),
            )
    print('Success!')
    print('Used time:', datetime.datetime.now() - start_time)


class Command(BaseCommand):
    async def handle(self, *args, **options):
        await parse()


main_loop = asyncio.get_event_loop()

if __name__ == "__main__":
    main_loop.run_until_complete(Command.handle())
