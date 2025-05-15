
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import User, Role, AgentProfile, BuyerProfile, SellerProfile, TenantProfile

@receiver(m2m_changed, sender=User.roles.through)
def create_profile_on_role_assignment(sender, instance, action, pk_set, **kwargs):
    if action != "post_add":
        return

    for role_id in pk_set:
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            continue

        role_name = role.name.lower()

        if role_name == 'agent' and not hasattr(instance, 'agent_profile'):
            AgentProfile.objects.get_or_create(user=instance, agent_id=f"AGENT-{instance.id}")
        elif role_name == 'buyer' and not hasattr(instance, 'buyer_profile'):
            BuyerProfile.objects.get_or_create(user=instance, buyer_id=f"BUYER-{instance.id}")
        elif role_name == 'tenant' and not hasattr(instance, 'tenant_profile'):
            TenantProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'phone': instance.phone or '0000000000',
                    'address': 'Default address',
                    'preferred_city': 'Default City',
                    'rental_budget_min': 0,
                    'rental_budget_max': 0
                }
            )
        elif role_name == 'seller' and not hasattr(instance, 'seller_profile'):
            SellerProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'phone': instance.phone or '0000000000',
                    'address': 'Default address'
                }
            )
