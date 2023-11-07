from .actions import export_as_csv_action


class ExportCsvMixin:
    """
    Mixin para adicionar a ação de exportação CSV a um ModelAdmin.
    """

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Adiciona a ação de exportação CSV
        actions["export_as_csv"] = (
            export_as_csv_action(),
            "export_as_csv",
            "Exportar itens selecionados para CSV",
        )
        return actions


class CompanyAdminMixin:
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
