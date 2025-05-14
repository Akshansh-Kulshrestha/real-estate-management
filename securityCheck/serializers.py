from rest_framework import serializers
from .models import Document, Verification
from django.contrib.auth import get_user_model
from core.serializers import PropertySerializer, UserSerializer

User = get_user_model()


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']


class VerificationSerializer(serializers.ModelSerializer):
    target_user = UserSerializer(read_only=True)
    target_property = PropertySerializer(read_only=True)

    class Meta:
        model = Verification
        fields = '__all__'
        read_only_fields = ['verified_at']
