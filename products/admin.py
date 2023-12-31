from django.contrib import admin

from core.auxiliar import AdminBase
from core.mixins.mixins import CompanyAdminMixin

from .models import Category, CategoryRecommendation, Product, ProductImage


class ProductImageInline(CompanyAdminMixin, admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(AdminBase):
    list_display = ("name", "company", "date_created")
    search_fields = ("name", "company__name")
    list_filter = ("company",)
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(AdminBase):
    list_display = ("name", "company", "date_created")
    search_fields = ("name", "company__name")
    list_filter = ("company",)
    filter_horizontal = ("products",)


@admin.register(CategoryRecommendation)
class CategoryRecommendationAdmin(AdminBase):
    list_display = (
        "category_a",
        "category_b",
        "recommendation_text",
        "company",
        "date_created",
    )
