from django.contrib import admin
from .models import MaintenanceRequest, MaintenanceLog, ServiceProvider

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tenant', 'property', 'status', 'assigned_provider', 'requested_at')
    list_filter = ('status', 'requested_at', 'assigned_provider')
    search_fields = ('title', 'description', 'tenant__user__username', 'property__title', 'assigned_provider__name')
    readonly_fields = ('requested_at', 'updated_at')
    date_hierarchy = 'requested_at'

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'maintenance_request', 'status', 'updated_by', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('maintenance_request__title', 'note', 'updated_by__username')
    readonly_fields = ('updated_at',)


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'service_type', 'phone', 'email', 'is_active')
    list_filter = ('service_type', 'is_active')
    search_fields = ('name', 'service_type', 'email', 'phone')




