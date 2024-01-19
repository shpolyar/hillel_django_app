from django.db import models
from djrichtextfield.models import RichTextField


class DataTimeStamp(models.Model):
    created = models.DateTimeField('Created', auto_now=True)
    updated = models.DateTimeField('Updated', auto_now_add=True)

    class Meta:
        abstract = True


class ExcelCategory(models.Model):
    name = models.CharField('id', max_length=10, unique=True)
    url = models.URLField('Url', blank=True)
    width = models.IntegerField('width', blank=True)
    height = models.IntegerField('height', blank=True)

    class Meta:
        verbose_name = 'Excel Category'
        verbose_name_plural = 'Excel Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Имя категории', max_length=25, unique=True)
    # url = models.URLField('Url', blank=True)
    # email = models.EmailField('Email', blank=True)
    description = RichTextField('Описание', blank=True)
    activate = models.BooleanField('Active', default=False)
    created = models.DateTimeField('Created', auto_now=True)
    updated = models.DateTimeField('Updated', auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/category_detail/{self.pk}/'


class Tag(models.Model):
    name = models.CharField('Имя тега', max_length=25, unique=True)
    uuid = models.UUIDField('UUID')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Parametr(models.Model):
    name = models.CharField('Параметр товару', max_length=25, unique=True)

    class Meta:
        verbose_name = 'Parametr'
        verbose_name_plural = 'Parametrs'
        ordering = ['name']

    def __str__(self):
        return self.name


class Goods(DataTimeStamp):
    name = models.CharField('Название товара', max_length=100, unique=True)
    # name = models.CharField('Название товара', max_length=100)
    description = RichTextField('Описание', blank=True)
    price = models.FloatField('Price', default=0)
    activate = models.BooleanField('Active', default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods')
    tags = models.ManyToManyField(Tag, related_name='goods_tag')
    image = models.ImageField('Image', upload_to='image', blank=True)
    parametr = models.ForeignKey(Parametr, on_delete=models.CASCADE, related_name='parametr', null=True, blank=True)

    class Meta:
        verbose_name = 'Good'
        verbose_name_plural = 'Goods'
        ordering = ['name']

    def __str__(self):
        return self.name
