from .models import Product, ProductImage, Category, CategoryAffinity
from django.contrib import admin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Número de linhas extras a serem mostradas.

class ProductClassAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Product)
class ProductAdmin(ProductClassAdmin):
    exclude = ('company',)  # Exclude the company field from the form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        elif hasattr(request.user, 'company'):
            return qs.filter(company=request.user.company)
        else:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            obj.company = request.user.company
        super().save_model(request, obj, form, change)
        
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('company',)  # Exclude the company field from the form
    filter_horizontal = ('products',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        elif hasattr(request.user, 'company'):
            return qs.filter(company=request.user.company)
        else:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            obj.company = request.user.company
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "affinity_categories":
            if request._obj_ is not None:
                kwargs["queryset"] = Category.objects.exclude(id=request._obj_.id)
            else:
                kwargs["queryset"] = Category.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


@admin.register(CategoryAffinity)
class CategoryAffinityAdmin(admin.ModelAdmin):
    exclude = ('company',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'employee'):
            return qs.filter(company=request.user.employee.company)
        else:
            return qs.filter(company=request.user.company)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["category1", "category2"]:
            if hasattr(request.user, 'employee'):
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.employee.company)
            else:
                kwargs["queryset"] = db_field.related_model.objects.filter(company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set the company when the object is first created
            if hasattr(request.user, 'employee'):
                obj.company = request.user.employee.company
            else:
                obj.company = request.user.company
        super().save_model(request, obj, form, change)