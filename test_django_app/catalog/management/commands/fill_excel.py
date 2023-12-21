from django.core.management.base import BaseCommand
import requests

from catalog.models import ExcelCategory

my_api_key = 'live_khzEGj4X6mNCSGri8mQaw9GPpWDr6EUGULS8AZM4CeFC6MH9ZhQlS6pJrMfF8NFv'

data = {
    'x-api-key': my_api_key,
}

url = f'https://api.thecatapi.com/v1/images/search?limit=15&breed_ids=beng&api_key={my_api_key}'


class Command(BaseCommand):
    help_text = 'Command to fill Excel Category'

    def handle(self, *args, **options):
        req = requests.get(url)
        print(req)
        if req.status_code == 200:
            cats = req.json()
            for item in cats:
                print(item['id'], item['url'], item['width'], item['height'])
                obj, created = ExcelCategory.objects.get_or_create(
                    name=item['id'],
                    url=item['url'],
                    width=item['width'],
                    height=item['height']
                )
        print('Finish')
