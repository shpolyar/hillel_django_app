from .models import Goods, Tag
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save, sender=Goods)
def handle(sender, **kwargs):
    print(f'Goods {sender.name} is created')


@receiver(post_save, sender=Tag)
def tag_handle(sender, **kwargs):
    # print(f'Tag {kwargs["instance"]} is created')
    send_mail(
        'Tag is created',
        f'Tag {kwargs["instance"]} is created',
        'from@yoyrdjangoapp.com',
        ['to@yourbestuser.com'],
        fail_silently=False
    )