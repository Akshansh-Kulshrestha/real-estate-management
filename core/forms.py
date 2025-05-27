from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm 
from .models import *

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
        fields = ['title', 'description', 'price_min','price_max', 'area_sqft', 'furnishing', 'bathrooms', 'bedrooms', 'location', 'Address', 'amenities', 'property_type' ]

class UserForm(forms.ModelForm):

    class Meta: 
        model= User
        fields = ['username','address', 'email', 'phone', 'state', 'city', 'image', 'first_name', 'last_name']

class LocationForm(forms.ModelForm):

    class Meta:
        model=Location
        fields = '__all__'



