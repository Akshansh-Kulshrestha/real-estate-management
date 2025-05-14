from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ServiceProvider, MaintenanceRequest, MaintenanceLog
from .serializers import (
    ServiceProviderSerializer,
    MaintenanceRequestSerializer,
    MaintenanceLogSerializer
)
from core.models import TenantProfile, Property
from django.shortcuts import get_object_or_404


class ServiceProviderAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            provider = get_object_or_404(ServiceProvider, pk=pk)
            serializer = ServiceProviderSerializer(provider)
        else:
            providers = ServiceProvider.objects.all()
            serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        provider = get_object_or_404(ServiceProvider, pk=pk)
        serializer = ServiceProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        provider = get_object_or_404(ServiceProvider, pk=pk)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaintenanceRequestAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            request_obj = get_object_or_404(MaintenanceRequest, pk=pk)
            serializer = MaintenanceRequestSerializer(request_obj)
        else:
            requests = MaintenanceRequest.objects.all()
            serializer = MaintenanceRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaintenanceRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.user.tenantprofile)  # adjust as needed
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        request_obj = get_object_or_404(MaintenanceRequest, pk=pk)
        serializer = MaintenanceRequestSerializer(request_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        request_obj = get_object_or_404(MaintenanceRequest, pk=pk)
        request_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaintenanceLogAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            log = get_object_or_404(MaintenanceLog, pk=pk)
            serializer = MaintenanceLogSerializer(log)
        else:
            logs = MaintenanceLog.objects.all()
            serializer = MaintenanceLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaintenanceLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        log = get_object_or_404(MaintenanceLog, pk=pk)
        serializer = MaintenanceLogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        log = get_object_or_404(MaintenanceLog, pk=pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
# from .models import ServiceProvider, MaintenanceRequest, MaintenanceLog
# from core.models import Property  # Assuming Property is defined in core.models

# # List all active service providers
# @login_required
# def service_provider_list(request):
#     providers = ServiceProvider.objects.filter(is_active=True)
#     data = [
#         {
#             "id": provider.id,
#             "name": provider.name,
#             "service_type": provider.service_type,
#             "phone": provider.phone,
#             "email": provider.email,
#         }
#         for provider in providers
#     ]
#     return JsonResponse({"service_providers": data})


# # List maintenance requests for the logged in tenant
# @login_required
# def maintenance_request_list(request):
#     try:
#         tenant = request.user.tenant_profile  # Assumes a OneToOneField exists between User and TenantProfile
#     except Exception:
#         return HttpResponse("No tenant profile found.", status=404)

#     requests_qs = MaintenanceRequest.objects.filter(tenant=tenant)
#     data = [
#         {
#             "id": req.id,
#             "title": req.title,
#             "status": req.status,
#             "requested_at": req.requested_at,
#         }
#         for req in requests_qs
#     ]
#     return JsonResponse({"maintenance_requests": data})


# # Detailed view for a specific maintenance request including logs
# @login_required
# def maintenance_request_detail(request, request_id):
#     req_obj = get_object_or_404(MaintenanceRequest, id=request_id)
#     # Check authorization: ensure the logged-in tenant owns this request
#     if hasattr(request.user, "tenant_profile") and req_obj.tenant != request.user.tenant_profile:
#         return HttpResponse("Not authorized to view this maintenance request.", status=403)

#     logs = req_obj.logs.all()
#     log_data = [
#         {
#             "id": log.id,
#             "note": log.note,
#             "status": log.status,
#             "updated_by": log.updated_by.username if log.updated_by else None,
#             "updated_at": log.updated_at,
#         }
#         for log in logs
#     ]
#     data = {
#         "id": req_obj.id,
#         "title": req_obj.title,
#         "description": req_obj.description,
#         "status": req_obj.status,
#         "requested_at": req_obj.requested_at,
#         "assigned_provider": req_obj.assigned_provider.name if req_obj.assigned_provider else None,
#         "logs": log_data,
#     }
#     return JsonResponse(data, safe=False)


# # Create a new maintenance request (for tenants)
# @csrf_exempt  # Use proper CSRF protection in production
# @login_required
# def create_maintenance_request(request):
#     if request.method == "POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         property_id = request.POST.get("property_id")
        
#         # Check for missing parameters
#         if not title or not description or not property_id:
#             return HttpResponse("Missing title, description, or property_id.", status=400)

#         try:
#             tenant = request.user.tenant_profile  # Tenant profile should exist for the logged in user
#         except Exception:
#             return HttpResponse("No tenant profile found.", status=404)

#         # Validate that property exists
#         try:
#             property_obj = Property.objects.get(id=property_id)
#         except Property.DoesNotExist:
#             return HttpResponse("Property not found.", status=404)
        
#         # Create maintenance request
#         request_obj = MaintenanceRequest.objects.create(
#             title=title,
#             description=description,
#             tenant=tenant,
#             property=property_obj,
#             requested_at=timezone.now()
#         )
#         return HttpResponse(f"Maintenance request '{request_obj.title}' created successfully.")
    
#     return HttpResponse("Use POST to create a maintenance request.")


# # Add a maintenance log to an existing request
# @csrf_exempt  # Use proper CSRF protection in production
# @login_required
# def add_maintenance_log(request, request_id):
#     if request.method == "POST":
#         req_obj = get_object_or_404(MaintenanceRequest, id=request_id)
#         note = request.POST.get("note")
#         status_val = request.POST.get("status")
        
#         if not note or not status_val:
#             return HttpResponse("Missing note or status.", status=400)
        
#         # Create a new maintenance log entry
#         log_entry = MaintenanceLog.objects.create(
#             maintenance_request=req_obj,
#             note=note,
#             status=status_val,
#             updated_by=request.user,
#             updated_at=timezone.now()
#         )
#         # Optionally update the status of the maintenance request as well
#         req_obj.status = status_val
#         req_obj.save()
        
#         return HttpResponse(f"Log added to maintenance request '{req_obj.title}'.")
    
#     return HttpResponse("Use POST to add a maintenance log.")
