from django.db import models
from django.utils import timezone
from core.models import *
from django.conf import settings


class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField(help_text="Annual interest rate in %")
    term_years = models.IntegerField(help_text="Loan term in years")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_interest(self):
        return (self.amount * self.interest_rate * self.term_years) / 100

    def total_repayment(self):
        return self.amount + self.total_interest()

    def monthly_installment(self):
        return self.total_repayment() / (self.term_years * 12)

    def __str__(self):
        return f"Loan for {self.property} by {self.user}"

class Booking(models.Model):
    buyer = models.ForeignKey('core.BuyerProfile', on_delete=models.CASCADE)
    agent = models.ForeignKey('core.AgentProfile', on_delete=models.CASCADE)
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.property.title} on {self.appointment_date}"

    def is_upcoming(self):
        return self.appointment_date > timezone.now()

class Offer(models.Model):
    buyer = models.ForeignKey('core.BuyerProfile', on_delete=models.CASCADE)
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE)
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    offer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer of {self.offer_amount} on {self.property.title} by {self.buyer.user.username}"

class Transaction(models.Model):
    buyer = models.ForeignKey('core.BuyerProfile', on_delete=models.CASCADE)
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer'), ('cash', 'Cash')])
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=50, choices=[('completed', 'Completed'), ('failed', 'Failed'), ('pending', 'Pending')], default='completed')

    def __str__(self):
        return f"Transaction of {self.amount} for {self.property.title} by {self.buyer.user.username}"

class LeaseAgreement(models.Model):
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE)
    tenant = models.ForeignKey('core.TenantProfile', on_delete=models.CASCADE)  # Assuming a buyer can also be a tenant
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    terms_and_conditions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lease Agreement for {self.property.title} with {self.tenant.user.username}"
    
    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date
