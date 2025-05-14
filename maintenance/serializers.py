from rest_framework import serializers
from .models import ServiceProvider, MaintenanceRequest, MaintenanceLog
from core.serializers import TenantProfileSerializer, PropertySerializer, UserSerializer


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'


class MaintenanceLogSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = MaintenanceLog
        fields = '__all__'
        read_only_fields = ['updated_at']


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant = TenantProfileSerializer(read_only=True)
    property = PropertySerializer(read_only=True)
    assigned_provider = ServiceProviderSerializer(read_only=True)
    logs = MaintenanceLogSerializer(many=True, read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
