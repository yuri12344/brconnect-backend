from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order, dispatch_uid="update_order_total_once")
def update_order_total(sender, instance, **kwargs):
    if "updating_total" not in kwargs:
        instance.total = instance.calculate_total()
        instance.amount_missing = instance.get_total_missing()
        # Passa um argumento adicional para evitar a chamada recursiva.
        instance.save(update_fields=["total", "amount_missing"], updating_total=True)
