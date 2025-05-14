from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Invoice

@receiver(post_save, sender=Payment)
def update_invoice_payment_status(sender, instance, **kwargs):
    invoice = instance.invoice
    total_paid = sum(payment.amount for payment in invoice.payments.all())
    invoice.is_paid = total_paid >= invoice.amount
    invoice.save()
