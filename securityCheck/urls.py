from django.urls import path
from .views import DocumentAPIView, VerificationAPIView

urlpatterns = [
    path('documents/', DocumentAPIView.as_view()),
    path('documents/<int:pk>/', DocumentAPIView.as_view()),
    path('verifications/', VerificationAPIView.as_view()),
    path('verifications/<int:pk>/', VerificationAPIView.as_view()),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload/', views.upload_document, name='upload_document'),
#     path('my-documents/', views.user_documents, name='user_documents'),
#     path('verify-document/<int:doc_id>/', views.verify_document, name='verify_document'),
#     path('request-verification/', views.request_verification, name='request_verification'),
#     path('verify-verification/<int:verification_id>/', views.verify_verification, name='verify_verification'),
#     path('pending-verifications/', views.pending_verifications, name='pending_verifications'),
# ]
