from .models import Product, ProductImage, Category
from django.contrib import admin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Número de linhas extras a serem mostradas.

class ProductBaseClassAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Product)
class ProductAdmin(ProductBaseClassAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
