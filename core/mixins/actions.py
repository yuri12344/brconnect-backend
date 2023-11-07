import csv

from django.http import HttpResponse
from django.utils.encoding import smart_str


def export_as_csv_action(
    description="Exportar itens selecionados para CSV",
    fields=None,
    exclude=None,
    header=True,
):
    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        field_names = (
            [field.name for field in opts.fields] if fields is None else fields
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            opts.verbose_name
        )

        writer = csv.writer(response)

        if header:
            writer.writerow([smart_str(label) for label in field_names])
        for obj in queryset:
            row = [smart_str(getattr(obj, field)) for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = description
    return export_as_csv
