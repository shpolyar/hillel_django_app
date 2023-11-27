from django.core.management.base import BaseCommand
from faker import Faker
import uuid
from catalog.models import Tag


fake = Faker()


class Command(BaseCommand):
    help_text = 'Command to fill the database'

    def handle(self, *args, **options):
        for _ in range(5):
            name = fake.domain_word()
            uuid_str = str(uuid.uuid4())
            Tag.objects.get_or_create(name=name, uuid=uuid_str)
        print("Finish creating Tags")
