from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from apps.products.models import Product, ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = ['name', 'count', 'price', 'enable']
    inlines = [ProductImageInline]
