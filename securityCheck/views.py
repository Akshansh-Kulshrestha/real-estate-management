from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Document, Verification
from .serializers import DocumentSerializer, VerificationSerializer


class DocumentAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            doc = get_object_or_404(Document, pk=pk)
            serializer = DocumentSerializer(doc)
        else:
            documents = Document.objects.all()
            serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        serializer = DocumentSerializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # You can restrict who can update verification status
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerificationAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            verification = get_object_or_404(Verification, pk=pk)
            serializer = VerificationSerializer(verification)
        else:
            verifications = Verification.objects.all()
            serializer = VerificationSerializer(verifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification = serializer.save()
            if request.data.get('is_verified'):
                verification.verified_at = timezone.now()
                verification.save()
            return Response(VerificationSerializer(verification).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        verification = get_object_or_404(Verification, pk=pk)
        serializer = VerificationSerializer(verification, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            if updated.is_verified and not updated.verified_at:
                updated.verified_at = timezone.now()
                updated.save()
            return Response(VerificationSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        verification = get_object_or_404(Verification, pk=pk)
        verification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from django.shortcuts import get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.http import HttpResponse
# from django.utils.timezone import now
# from .models import Document, Verification
# from core.models import Property  # Assuming you have Property model in core app

# # ---------- DOCUMENT VIEWS ----------

# @login_required
# def upload_document(request):
#     if request.method == "POST":
#         document_type = request.POST.get("document_type")
#         file = request.FILES.get("file")

#         if not document_type or not file:
#             return HttpResponse("Missing document_type or file", status=400)

#         Document.objects.create(
#             uploaded_by=request.user,
#             document_type=document_type,
#             file=file
#         )
#         return HttpResponse("Document uploaded successfully.")
    
#     return HttpResponse("Invalid request method.", status=405)


# @login_required
# def user_documents(request):
#     documents = Document.objects.filter(uploaded_by=request.user)
#     if documents.exists():
#         return HttpResponse(f"Documents: {', '.join([doc.document_type for doc in documents])}")
#     else:
#         return HttpResponse("No documents found.")


# # Admin view to verify a document
# @permission_required('verification.change_document')
# def verify_document(request, doc_id):
#     document = get_object_or_404(Document, id=doc_id)
#     if request.method == "POST":
#         document.is_verified = True
#         document.save()
#         return HttpResponse(f"Document {document.id} verified.")
    
#     return HttpResponse("Invalid request method.", status=405)


# # ---------- VERIFICATION VIEWS ----------

# @login_required
# def request_verification(request):
#     if request.method == "POST":
#         verification_type = request.POST.get("verification_type")
#         notes = request.POST.get("notes", "")
#         prop_id = request.POST.get("property_id")

#         if verification_type == "user":
#             Verification.objects.create(
#                 verification_type="user",
#                 target_user=request.user,
#                 notes=notes
#             )
#         elif verification_type == "property" and prop_id:
#             prop = get_object_or_404(Property, id=prop_id)
#             Verification.objects.create(
#                 verification_type="property",
#                 target_user=request.user,
#                 target_property=prop,
#                 notes=notes
#             )
#         else:
#             return HttpResponse("Invalid request data", status=400)

#         return HttpResponse("Verification request submitted.")

#     return HttpResponse("Invalid request method.", status=405)


# # Admin view to verify user or property
# @permission_required('verification.change_verification')
# def verify_verification(request, verification_id):
#     verification = get_object_or_404(Verification, id=verification_id)
#     if request.method == "POST":
#         verification.is_verified = True
#         verification.verified_at = now()
#         verification.save()
#         return HttpResponse(f"{verification.verification_type.capitalize()} verified.")
    
#     return HttpResponse("Invalid request method.", status=405)


# # Admin view: list all pending verifications
# @permission_required('verification.view_verification')
# def pending_verifications(request):
#     verifications = Verification.objects.filter(is_verified=False)
#     if verifications.exists():
#         verification_list = ', '.join([f"{verif.verification_type} for {verif.target_user}" for verif in verifications])
#         return HttpResponse(f"Pending verifications: {verification_list}")
#     else:
#         return HttpResponse("No pending verifications.")
