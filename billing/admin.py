from django.contrib import admin
from .models import Invoice, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'due_date', 'is_paid')
    list_filter = ('is_paid', 'due_date')
    search_fields = ('id',)
    inlines = [PaymentInline]
    readonly_fields = ('is_paid',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'payment_date')
    list_filter = ('payment_date',)
    search_fields = ('invoice__id',)

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
