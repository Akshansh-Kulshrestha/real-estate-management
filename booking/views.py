from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, Booking, Offer, Transaction, LeaseAgreement
from .serializers import LoanSerializer, BookingSerializer, OfferSerializer, TransactionSerializer, LeaseAgreementSerializer


class LoanAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            loan = Loan.objects.get(pk=pk)
            serializer = LoanSerializer(loan)
        else:
            loans = Loan.objects.all()
            serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        loan = Loan.objects.get(pk=pk)
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        loan = Loan.objects.get(pk=pk)
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            booking = Booking.objects.get(pk=pk)
            serializer = BookingSerializer(booking)
        else:
            bookings = Booking.objects.all()
            serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            offer = Offer.objects.get(pk=pk)
            serializer = OfferSerializer(offer)
        else:
            offers = Offer.objects.all()
            serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        serializer = OfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            transaction = Transaction.objects.get(pk=pk)
            serializer = TransactionSerializer(transaction)
        else:
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaseAgreementAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            lease_agreement = LeaseAgreement.objects.get(pk=pk)
            serializer = LeaseAgreementSerializer(lease_agreement)
        else:
            lease_agreements = LeaseAgreement.objects.all()
            serializer = LeaseAgreementSerializer(lease_agreements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaseAgreementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        lease_agreement = LeaseAgreement.objects.get(pk=pk)
        serializer = LeaseAgreementSerializer(lease_agreement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lease_agreement = LeaseAgreement.objects.get(pk=pk)
        lease_agreement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# # views.py
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from .models import Loan, Booking, Offer, Transaction, LeaseAgreement
# from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone

# # LOANS
# @login_required
# def user_loans(request):
#     loans = Loan.objects.filter(user=request.user)
#     return HttpResponse(f"You have {loans.count()} loan(s).")

# # BOOKINGS
# @login_required
# def user_bookings(request):
#     bookings = Booking.objects.filter(buyer__user=request.user)
#     return HttpResponse(f"You have {bookings.count()} booking(s).")

# # OFFERS
# @login_required
# def user_offers(request):
#     offers = Offer.objects.filter(buyer__user=request.user)
#     return HttpResponse(f"You made {offers.count()} offer(s).")

# # TRANSACTIONS
# @login_required
# def user_transactions(request):
#     transactions = Transaction.objects.filter(buyer__user=request.user)
#     return HttpResponse(f"You have {transactions.count()} transaction(s).")

# # LEASE AGREEMENTS
# @login_required
# def user_leases(request):
#     leases = LeaseAgreement.objects.filter(tenant__user=request.user)
#     active_count = sum([1 for lease in leases if lease.is_active()])
#     return HttpResponse(f"You have {leases.count()} lease(s), {active_count} of them active.")
