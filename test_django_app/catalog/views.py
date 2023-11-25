from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Goods, Tag
from .serializers import CategorySerializer, TagSerializer, GoodsSerializer


# Create your views here.
class CategoryViews(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(activate=True).order_by('id')




class TagViews(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.order_by('id')


class GoodsViews(viewsets.ModelViewSet):
    serializer_class = GoodsSerializer
    queryset = Goods.objects.filter(activate=True).order_by('id')
