from django.contrib import admin
from .models import *
from decimal import Decimal
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.forms.widgets import CheckboxSelectMultiple

class GroupedPermissionForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
            'permissions': CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Group permissions by model
        grouped_permissions = {}
        for perm in Permission.objects.select_related('content_type'):
            model_name = perm.content_type.model.capitalize()
            grouped_permissions.setdefault(model_name, []).append(perm)

        # Flatten grouped perms into choices
        choices = []
        for model, perms in grouped_permissions.items():
            perms_list = [(p.id, p.name) for p in perms]
            choices.append((model, perms_list))

        self.fields['permissions'].choices = choices

class RoleAdmin(admin.ModelAdmin):
    form = GroupedPermissionForm
    filter_horizontal = ()  # Remove filter widget

    class Media:
        js = ('admin/js/role_permissions.js',)
admin.site.register(Role, RoleAdmin)


class CustomUserAdmin(BaseUserAdmin):
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {
            'fields': ('phone', 'image', 'roles'),
        }),
    )
    filter_horizontal = ('roles',)

admin.site.register(User, CustomUserAdmin)

class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_phone')

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

admin.site.register(AgentProfile, AgentProfileAdmin)


class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_phone', 'preferred_city')

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

admin.site.register(BuyerProfile, BuyerProfileAdmin)  # Register BuyerProfile once


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Display at least one empty form to add images

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('location', 'area_sqft', 'property_type', 'price_per_sqft')
    inlines =[PropertyImageInline]
    
    @admin.display(description='Price / Sqft')
    def price_per_sqft(self, obj):
        # Ensure both are of the same type (Decimal)
        if obj.area_sqft:
            return Decimal(obj.price) / Decimal(obj.area_sqft)  # Convert both to Decimal
        return '-'


admin.site.register(Property, PropertyAdmin)  # Register the Property model

# TenantProfile Admin
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'preferred_city', 'rental_budget_min', 'rental_budget_max')
    search_fields = ('user__username', 'preferred_city', 'phone')
    list_filter = ('preferred_city',)

admin.site.register(TenantProfile, TenantProfileAdmin)

# SellerProfile Admin
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone', 'address')
    list_filter = ('user__username',)

admin.site.register(SellerProfile, SellerProfileAdmin)

# Register other models
admin.site.register(Amenity)
admin.site.register(Location)
admin.site.register(PropertyImage)
admin.site.register(PropertyType)
