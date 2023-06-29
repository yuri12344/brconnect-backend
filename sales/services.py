from .models import Product

def get_affinity_products(category):
    """
    Get products from affinity categories.
    """
    products = Product.objects.filter(categories__in=category.affinity_categories.all())
    return products

