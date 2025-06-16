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

from django.contrib import admin
from .models import User, Role, UserRole

class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'role__name')


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserRoleInline]
    list_display = ('username', 'email', 'get_roles')

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    get_roles.short_description = 'Roles'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)

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


# Inline for PropertyImage
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Number of empty forms to show
    fields = ('image',)

# Inline for Nearby Places
class NearbyPlaceInline(admin.TabularInline):
    model = NearbyPlace
    extra = 1

# Admin for Property
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_min', 'price_max', 'bedrooms', 'bathrooms', 'status', 'is_featured')
    list_filter = ('status', 'location', 'property_type', 'listing_type', 'furnishing')
    search_fields = ('title', 'Address', 'location__name', 'description')
    inlines = [PropertyImageInline, NearbyPlaceInline]
    readonly_fields = ('date_posted',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'property_type', 'listing_type', 'status', 'is_featured')
        }),
        ('Pricing & Area', {
            'fields': ('price_min', 'price_max', 'area_sqft')
        }),
        ('Details', {
            'fields': ('bedrooms', 'bathrooms', 'furnishing', 'amenities')
        }),
        ('Location Info', {
            'fields': ('Address', 'location')
        }),
        ('Media', {
            'fields': ('video_url', 'highlights')
        }),
        ('Ownership & Posting', {
            'fields': ('user', 'owner', 'date_posted')
        }),
    )

# Optional: You can register these separately as well if needed
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property',  'image')
    list_filter = ( 'property',)

@admin.register(NearbyPlace)
class NearbyPlaceAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'distance_km', 'place_type')
    list_filter = ('place_type',)
    search_fields = ('name', 'property__title')

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
admin.site.register(PropertyType)
