from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Verification
from django.utils.timezone import now

@receiver(pre_save, sender=Verification)
def auto_set_verified_at(sender, instance, **kwargs):
    if instance.is_verified and instance.verified_at is None:
        instance.verified_at = now()
