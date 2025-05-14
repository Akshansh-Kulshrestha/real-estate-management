from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.name


# Abstract user
class AbstractCustomUser(AbstractUser):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'roles__name__in': ['superadmin', 'agent', 'seller', 'buyer', 'tenant', 'landlord', 'manager']},
        related_name='created_users',
    )

    def __str__(self):
        return self.username or self.email
    class Meta:
        abstract = True

# Main user
class User(AbstractCustomUser):
    roles = models.ManyToManyField(Role, related_name='users')
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to='user/', blank=True, null=True)

    def __str__(self):
        return self.username or self.email

    def has_role(self, role):
        return self.roles.filter(name=role).exists()

    def add_role(self, role_name):
        role, _ = Role.objects.get_or_create(name=role_name)
        self.roles.add(role)

    def remove_role(self, role_name):
        role = Role.objects.filter(name=role_name).first()
        if role:
            self.roles.remove(role)

# Agent Profile
class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    agent_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Agent: {self.user.username} ({self.agent_id})"

# Buyer Profile
class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    buyer_id = models.CharField(max_length=100, unique=True)
    preferred_city = models.CharField(max_length=100, blank=True)
    budget_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Buyer: {self.user.username} ({self.buyer_id})"

# Tenant Profile
class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    preferred_city = models.CharField(max_length=100)
    rental_budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    rental_budget_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Tenant: {self.user.username} - {self.preferred_city}"

# Seller Profile
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    # Assuming Property model exists
    properties_for_sale = models.ManyToManyField('Property', related_name='sellers')

    def __str__(self):
        return f"Seller: {self.user.username} - {self.phone}"


#property type
class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#location
class Location(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.area}, {self.city}, {self.state}, {self.country}, {self.pincode}"

#Amenity
class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#Property
class Property(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area_sqft = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    furnishing = models.CharField(max_length=50, choices=[
        ('unfurnished', 'Unfurnished'),
        ('semi-furnished', 'Semi-Furnished'),
        ('furnished', 'Furnished'),
    ])
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    agent = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': 'agent'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    
    class Meta:
        permissions = [
            ('can_approve_property', 'Can approve property'),
            ('can_feature_property', 'Can feature property'),
            ('can_sell_property', 'Can mark property as sold'),
        ]

    def __str__(self):
        return self.title
    
 #Propert Image   
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"


    
