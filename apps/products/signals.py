from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.models import Product, ProductMetrics


@receiver(post_save, sender=Product)
def ensure_product_metrics(sender, instance: Product, created: bool, **kwargs):
    if created:
        ProductMetrics.objects.create(product=instance)
