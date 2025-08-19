from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from apps.review.models import Review


@receiver(pre_save, sender=Review)
def capture_old_rating(sender, instance, **kwargs):
    """Capture old rating before save"""
    if instance.pk:
        try:
            old = Review.objects.get(pk=instance.pk)
            instance._old_rating = old.rating
            instance._old_approved = old.is_approved
        except Review.DoesNotExist:
            pass

@receiver(post_save, sender=Review)
def handle_review_change(sender, instance, created, **kwargs):
    """Handle review create/update"""
    old_rating = getattr(instance, '_old_rating', None)
    instance.update_product_rating(old_rating)

@receiver(post_delete, sender=Review)
def handle_review_delete(sender, instance, **kwargs):
    """Handle review deletion"""
    instance.is_active = False
    instance.update_product_rating()