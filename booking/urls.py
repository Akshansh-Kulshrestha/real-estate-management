from django.urls import path
from .views import LoanAPIView, BookingAPIView, OfferAPIView, TransactionAPIView, LeaseAgreementAPIView

urlpatterns = [
    path('loans/', LoanAPIView.as_view()),
    path('loans/<int:pk>/', LoanAPIView.as_view()),

    path('bookings/', BookingAPIView.as_view()),
    path('bookings/<int:pk>/', BookingAPIView.as_view()),

    path('offers/', OfferAPIView.as_view()),
    path('offers/<int:pk>/', OfferAPIView.as_view()),

    path('transactions/', TransactionAPIView.as_view()),
    path('transactions/<int:pk>/', TransactionAPIView.as_view()),

    path('lease-agreements/', LeaseAgreementAPIView.as_view()),
    path('lease-agreements/<int:pk>/', LeaseAgreementAPIView.as_view()),
]

# # urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('loans/', views.user_loans, name='user_loans'),
#     path('bookings/', views.user_bookings, name='user_bookings'),
#     path('offers/', views.user_offers, name='user_offers'),
#     path('transactions/', views.user_transactions, name='user_transactions'),
#     path('leases/', views.user_leases, name='user_leases'),
# ]
