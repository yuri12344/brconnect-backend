# services.py
from .models import WhatsAppProductInfo

def create_whatsapp_product_info_in_db(product, whatsapp_id):
    """
    Create a WhatsAppProductInfo instance for a product in the database.
    """
    whatsapp_info = WhatsAppProductInfo.objects.create(product=product, whatsapp_id=whatsapp_id)
    return whatsapp_info

def add_images_to_whatsapp_product_info_in_db(product, images):
    """
    Add images to the WhatsAppProductInfo instance for a product in the database.
    """
    if hasattr(product, 'whatsapp_info'):
        product.whatsapp_info.whatsapp_images.add(*images)
    else:
        raise Exception('WhatsAppProductInfo instance does not exist for this product. Please create it first in the database.')

def add_all_images_to_whatsapp_product_info_in_db(product):
    """
    Add all images of a product to the WhatsAppProductInfo instance in the database.
    """
    add_images_to_whatsapp_product_info_in_db(product, product.images.all())
    