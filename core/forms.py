from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm 
from .models import *
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your registered email',
            'autocomplete': 'email'
        })
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    new_password1 = forms.CharField(label="Reset Password", widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'city', 'state', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields =['username', 'password']


class AgentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','address', 'email', 'phone', 'state', 'city', 'image', 'first_name', 'last_name']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price_min', 'price_max', 'area_sqft',
            'furnishing', 'bathrooms', 'bedrooms', 'location', 'Address',
            'amenities', 'property_type', 'owner',
            'video_url', 'highlights', 'listing_type'
        ]


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PropertyForm, self).__init__(*args, **kwargs)

        if user and user.is_superuser:
            self.fields['owner'].queryset = User.objects.filter(roles__name__in=['Agent', 'Seller']).distinct()
        else:
            self.fields['owner'].widget = forms.HiddenInput()
            self.fields['owner'].required = False
class UserForm(forms.ModelForm):

    class Meta: 
        model= User
        fields = ['username','address', 'email', 'phone', 'state', 'city', 'image', 'first_name', 'last_name']

class LocationForm(forms.ModelForm):

    class Meta:
        model=Location
        fields = '__all__'

class NearbyForm(forms.ModelForm):
    class Meta:
        model = NearbyPlace
        fields = ['name', 'distance_km', 'place_type'] 

