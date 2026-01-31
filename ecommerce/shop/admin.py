from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id')
    list_filter = ('price',)
    search_fields = ('name', 'description')
    ordering = ('name',)
