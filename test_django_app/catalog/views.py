from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
# from rest_framework.pagination import PageNumberPagination
from .models import Category, Goods, Tag
from .serializers import CategorySerializer, TagSerializer, GoodsSerializer
from .filters import GoodsFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class CategoryViews(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(activate=True).order_by('id').prefetch_related('goods', 'good__tags')


class TagViews(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.order_by('id')


class GoodsViews(viewsets.ModelViewSet):
    serializer_class = GoodsSerializer
    queryset = Goods.objects.filter(activate=True).order_by('id').prefetch_related('tags').select_related('category')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_class = GoodsFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
