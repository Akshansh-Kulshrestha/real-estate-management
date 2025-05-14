from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    issued_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.user.username}"

    class Meta:
        ordering = ['-issued_date']


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('online_wallet', 'Online Wallet'),
    ])
    transaction_id = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount} by {self.user.username}"

    class Meta:
        ordering = ['-payment_date']


# SIGNAL TO AUTO-UPDATE INVOICE STATUS
@receiver(post_save, sender=Payment)
def update_invoice_status(sender, instance, **kwargs):
    invoice = instance.invoice
    total_paid = sum(p.amount for p in invoice.payments.all())
    if total_paid >= invoice.amount:
        invoice.is_paid = True
        invoice.save()


