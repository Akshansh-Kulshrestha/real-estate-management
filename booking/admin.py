from django.contrib import admin
from .models import Booking, Offer, Transaction, LeaseAgreement, Loan

class BookingAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'agent', 'property', 'appointment_date', 'status', 'created_at')
    list_filter = ('status', 'appointment_date')
    search_fields = ('buyer__user__username', 'agent__user__username', 'property__title')

admin.site.register(Booking, BookingAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'property', 'offer_amount', 'status', 'offer_date')
    list_filter = ('status', 'offer_date')
    search_fields = ('buyer__user__username', 'property__title')

admin.site.register(Offer, OfferAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'property', 'amount', 'payment_method', 'transaction_status', 'transaction_date')
    list_filter = ('payment_method', 'transaction_status')
    search_fields = ('buyer__user__username', 'property__title')

admin.site.register(Transaction, TransactionAdmin)

class LeaseAgreementAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property', 'start_date', 'end_date', 'rent_amount', 'is_active')
    list_filter = ('start_date', 'end_date')
    search_fields = ('tenant__user__username', 'property__title')

admin.site.register(LeaseAgreement, LeaseAgreementAdmin)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'amount', 'interest_rate', 'term_years', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'property__title') 