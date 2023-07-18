from .models import Product, ProductImage, Category, CategoryRecommendation
from core.auxiliar import CompanyAdminMixin, AdminBase
from django.contrib import admin


class ProductImageInline(CompanyAdminMixin, admin.StackedInline):
    model = ProductImage
    extra = 1
    
@admin.register(Product)
class ProductAdmin(AdminBase):
    list_display = ('name', 'company', 'date_created')
    search_fields = ('name', 'company__name')
    list_filter = ('company',)
    inlines = [ProductImageInline]
    

@admin.register(Category)
class CategoryAdmin(AdminBase):
    list_display = ('name', 'company', 'date_created')
    search_fields = ('name', 'company__name')
    list_filter = ('company',)
    filter_horizontal = ('products',)

@admin.register(CategoryRecommendation)
class CategoryRecommendationAdmin(AdminBase):
    list_display = ('category_a', 'category_b', 'company', 'date_created')
    