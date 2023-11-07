import csv

import ipdb
from django.core.management import BaseCommand

from products.models import Product
from users.models import Supplier


class Command(BaseCommand):
    help = "Create suppliers from whatsapp orders"
    suppliers_csv_path = "users/files/suppliers/suppliers.csv"

    def handle(self, *args, **options):
        with open(self.suppliers_csv_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                products = Product.objects.filter(name=row["produtos"])
                if len(products) == 0:
                    print(f"{row['produtos']}")
