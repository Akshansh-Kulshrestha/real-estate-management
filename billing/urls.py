from django.urls import path
from .views import InvoiceAPIView, PaymentAPIView

urlpatterns = [
    path('invoices/', InvoiceAPIView.as_view()),
    path('invoices/<int:pk>/', InvoiceAPIView.as_view()),
    
    path('payments/', PaymentAPIView.as_view()),
    path('payments/<int:pk>/', PaymentAPIView.as_view()),
]


# # billing/urls.py

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('invoice/<int:invoice_id>/receipt/', views.download_receipt, name='download_receipt'),
#     path('invoices/', views.invoice_list, name='invoice_list'),
#     path('payments/', views.payment_list, name='payment_list'),
#     path('payments/create/', views.create_payment, name='create_payment'),
# ]
