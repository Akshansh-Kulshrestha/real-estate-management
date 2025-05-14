from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Token.objects.create(user=user)  # Automatically create token
        return user

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

# --- Basic Nested Serializers --- #

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'country', 'state', 'city', 'area', 'pincode']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image']

# --- Property Serializer --- #

class PropertySerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    agent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'area_sqft',
            'bedrooms', 'bathrooms', 'furnishing',
            'property_type', 'location', 'amenities',
            'agent', 'status', 'is_featured', 'date_posted'
        ]

# Optional: For creation via POST/PUT with IDs
class PropertyCreateSerializer(serializers.ModelSerializer):
    property_type = serializers.PrimaryKeyRelatedField(queryset=PropertyType.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    amenities = serializers.PrimaryKeyRelatedField(many=True, queryset=Amenity.objects.all())
    agent = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles__name='agent'))

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'area_sqft',
            'bedrooms', 'bathrooms', 'furnishing',
            'property_type', 'location', 'amenities',
            'agent', 'status', 'is_featured'
        ]

# --- Profile Serializers --- #

class SellerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'phone', 'address', 'properties_for_sale']

class AgentProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AgentProfile
        fields = ['id', 'user', 'agent_id']

class BuyerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BuyerProfile
        fields = [
            'id', 'user', 'buyer_id', 'preferred_city',
            'budget_range_min', 'budget_range_max'
        ]

class TenantProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TenantProfile
        fields = [
            'id', 'user', 'phone', 'address', 'preferred_city',
            'rental_budget_min', 'rental_budget_max'
        ]
