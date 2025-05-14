from rest_framework import serializers
from .models import Loan, Booking, Offer, Transaction, LeaseAgreement
from core.serializers import PropertySerializer, BuyerProfileSerializer, AgentProfileSerializer, TenantProfileSerializer


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    buyer = BuyerProfileSerializer()
    agent = AgentProfileSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    buyer = BuyerProfileSerializer()

    class Meta:
        model = Offer
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    buyer = BuyerProfileSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class LeaseAgreementSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    tenant = TenantProfileSerializer()

    class Meta:
        model = LeaseAgreement
        fields = '__all__'
