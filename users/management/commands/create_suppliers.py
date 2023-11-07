import csv

import ipdb
from django.core.management import BaseCommand

from products.models import Product
from users.models import Supplier, SupplierProduct


class Command(BaseCommand):
    help = "Create suppliers from whatsapp orders"
    suppliers_csv_path = "users/files/suppliers/suppliers.csv"

    def handle(self, *args, **options):
        with open(self.suppliers_csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                product = Product.objects.get(name=row["produtos"])
                supplier, created = Supplier.objects.get_or_create(
                    company_id=1, name=row["Nome fornecedor"]
                )

                supplier_product, sp_created = SupplierProduct.objects.get_or_create(
                    company_id=1,
                    supplier=supplier,
                    product=product,
                    defaults={"description": row["Descrição extra para fornecedor"]},
                )

                if not sp_created:
                    supplier_product.description = row[
                        "Descrição extra para fornecedor"
                    ]
                    supplier_product.save()

                if created:
                    print(
                        f"Fornecedor {supplier.name} criado com o produto {product.name}."
                    )
                else:
                    print(
                        f"Fornecedor {supplier.name} atualizado com o produto {product.name}."
                    )
