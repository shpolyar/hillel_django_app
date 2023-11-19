from django.contrib import admin
from .models import Category, Goods, Tag
import admin_thumbnails


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'activate', 'created', 'updated']
    list_filter = ['activate']
    search_fields = ['name', 'description']


@admin_thumbnails.thumbnail('image')
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'activate', 'category', 'created', 'updated']
    list_filter = ['activate', 'category']
    search_fields = ['name', 'description']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Tag)

admin.site.site_header = 'Admin Django'
admin.site.index_title = 'Welcome to Admin Portal'
