from django.contrib import admin


class AdminBase(admin.ModelAdmin):
    exclude = ("company",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.user.company)

    def save_model(self, request, obj, form, change):
        if not obj.company_id:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)
