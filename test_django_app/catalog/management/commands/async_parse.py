from urllib.parse import urljoin
from catalog.models import Category, Goods
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.defaultfilters import slugify
from transliterate import translit
import datetime
import asyncio
import aiohttp
import aiofiles
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async

URL = 'https://ukrzoloto.ua'


class Command(BaseCommand):
    @staticmethod
    async def req_body(url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:

        # async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                body = await resp.text()
                return body

    @staticmethod
    async def download_image(good_img_url, image_name):
        async with aiohttp.ClientSession as session:
            async with session.get(good_img_url) as resp:
                img_data = await resp.read()
        image_src = f'{settings.BASE_DIR}/media/image/{image_name}.jpg'
        async with aiofiles.open(image_src, 'wb') as handler:
            await handler.write(img_data)
        return f'image/{image_name}.jpg'

    @staticmethod
    def translit_word(name):
        return translit(name, 'ru', reversed=True)

    # @sync_to_async
    async def parse(self):
        tasks = []
        start_time = datetime.datetime.now()
        print('Start!')
        content = await self.req_body(URL + '/catalog')
        bs = BeautifulSoup(content, 'html5lib')
        for category_num, item in enumerate(bs.find_all("a", {"class": "catalogue-categories__link"})):
            if category_num == 5:
                break
            name = item.get_text()
            activate = True
            url = urljoin(URL, item.get('href'))
            category, created = await Category.objects.aget_or_create(
                name=name,
                activate=activate,
                description=url,
            )
            good_content = await self.req_body(url)
            bs1 = BeautifulSoup(good_content, 'html5lib')
            for good_num, good in enumerate(bs1.find_all("div", {"class": "product-card__content"})):
                if good_num == 10:
                    break
                good_name = good.select_one('.title').get_text()
                good_img_url = good.select_one('.image').get('src')
                good_price = good.select_one('.price__current span').get_text().replace(' ', '')
                await Goods.objects.aget_or_create(
                    name=f'{good_name}_{good_num}',
                    description=self.translit_word(good_name),
                    price=good_price,
                    activate=True,
                    category=category,
                    # image=self.download_image(good_img_url, slugify(self.translit_word(good_name))),
                )
                # task = asyncio.create_task()
                # tasks.append(task)

        print('Success!')
        # await asyncio.gather(*tasks)
        print('Used time:', datetime.datetime.now() - start_time)


    def handle(self, *args, **options):
        main_loop = asyncio.get_event_loop()

        # main_loop.run_forever()
        main_loop.run_until_complete(self.parse())
        # self.parse()
