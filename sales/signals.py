from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def update_order_total(sender, instance, **kwargs):
    # Verifica se a instância já tem um total calculado para evitar recálculo desnecessário.
    if not instance.total:
        instance.total = instance.calculate_total()
        instance.amount_missing = instance.get_total_missing()
        # Use update_fields para economizar recursos, atualizando apenas os campos necessários.
        instance.save(update_fields=['total', 'amount_missing'])