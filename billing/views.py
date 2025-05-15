from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer

# Base class reused for CRUD
class BaseAPIView(APIView):
    model_class = None
    serializer_class = None

    def get_object(self, pk):
        try:
            return self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            obj = self.get_object(pk)
            if not obj:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(obj)
        else:
            queryset = self.model_class.objects.all()
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvoiceAPIView(BaseAPIView):
    model_class = Invoice
    serializer_class = InvoiceSerializer
    def get_queryset(self, request):
        return Invoice.objects.filter(created_by=request.user)


class PaymentAPIView(BaseAPIView):
    model_class = Payment
    serializer_class = PaymentSerializer
    def get_queryset(self, request):
        return Payment.objects.filter(created_by=request.user)


# # billing/views.py

# from django.shortcuts import get_object_or_404
# from .utils import render_to_pdf
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from .models import Invoice, Payment
# from django.utils import timezone
# import uuid

# def download_receipt(request, invoice_id):
#     invoice = get_object_or_404(Invoice, id=invoice_id)
#     pdf = render_to_pdf('billing/receipt.html', {'invoice': invoice})
#     return pdf

# # views.py

# @login_required
# def invoice_list(request):
#     invoices = Invoice.objects.filter(user=request.user)
#     return HttpResponse(f"You have {invoices.count()} invoice(s).")

# @login_required
# def payment_list(request):
#     payments = Payment.objects.filter(user=request.user)
#     return HttpResponse(f"You have made {payments.count()} payment(s).")

# @csrf_exempt  # Remove in production or handle CSRF properly
# @login_required
# def create_payment(request):
#     if request.method == 'POST':
#         try:
#             invoice_id = request.POST.get('invoice_id')
#             amount = request.POST.get('amount')
#             method = request.POST.get('method')
#             notes = request.POST.get('notes', '')

#             invoice = Invoice.objects.get(id=invoice_id, user=request.user)

#             payment = Payment.objects.create(
#                 invoice=invoice,
#                 user=request.user,
#                 amount=amount,
#                 method=method,
#                 transaction_id=str(uuid.uuid4()),
#                 notes=notes,
#                 payment_date=timezone.now()
#             )

#             return HttpResponse(f"Payment of {amount} submitted successfully for Invoice #{invoice.invoice_number}.")

#         except Invoice.DoesNotExist:
#             return HttpResponse("Invoice not found or does not belong to you.", status=404)
#         except Exception as e:
#             return HttpResponse(f"Error: {str(e)}", status=500)

#     return HttpResponse("Use POST to submit a payment.")
