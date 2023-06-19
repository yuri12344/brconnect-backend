from django.contrib import admin
from .models import Category, Product, Ticket, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Número de linhas extras a serem mostradas.

class ProductBaseClassAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(ProductBaseClassAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(ProductBaseClassAdmin):
    fields = ('name', 'price', 'half_entry_price', 'description', 'category', 'commission', 'active', 'tags')
    pass
