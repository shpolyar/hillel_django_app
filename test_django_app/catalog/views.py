from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
# from rest_framework.pagination import PageNumberPagination
from .models import Category, Goods, Tag, ExcelCategory
from .serializers import CategorySerializer, TagSerializer, GoodsSerializer, ExcelCategorySerializer
from .filters import GoodsFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class ExcelCategoryView(viewsets.ModelViewSet):
    serializer_class = ExcelCategorySerializer
    queryset = ExcelCategory.objects.order_by('id')
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViews(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(activate=True).order_by('id').prefetch_related('goods', 'goods__tags')
    # permission_classes = [IsAuthenticatedOrReadOnly]


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

    # @method_decorator(cache_page(60*2))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class HelloViews(TemplateView):
    template_name = 'hello.html'


class CategoryListViews(ListView):
    model = Category
    template_name = 'category_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Category.objects.all()  # filter(activate=True)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = kwargs['object'].goods.count()
        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_create.html'
    fields = ['name', 'description', 'activate']


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category_update.html'
    fields = ['name', 'description', 'activate']
    success_url = '/category-list'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = '/category-list'
