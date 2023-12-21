from rest_framework import serializers
from .models import Category, Goods, Tag, ExcelCategory


class ExcelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelCategory
        fields = ['id', 'name', 'url', 'width', 'height']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'uuid']


class GoodsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Goods
        fields = ['id', 'name', 'description', 'price', 'activate', 'created', 'image',
                  'category', 'tags', 'parametr']


class CategorySerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=True, read_only=True)
    goods_count = serializers.SerializerMethodField('get_goods_count')

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'activate', 'created', 'goods', 'goods_count']

    def get_goods_count(self, category):
        count = category.goods.count()
        return count
