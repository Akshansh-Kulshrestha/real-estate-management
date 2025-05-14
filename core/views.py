from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from booking.models import *
from blog.models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                'message': 'User registered successfully.',
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })

class LogoutAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_role = user.roles.first().name if user.roles.exists() else "N/A"

        data = {
            "username": user.username,
            "email": user.email,
            "role": user_role,
            "total_properties": Property.objects.filter(created_by=user).count(),
            "total_bookings": Booking.objects.filter(buyer__user=user).count(),
            "pending_bookings": Booking.objects.filter(buyer__user=user, status='scheduled').count(),
            "total_transactions": Transaction.objects.filter(buyer__user=user).count(),
            "unread_messages": Message.objects.filter(recipient=user, is_read=False).count(),
            "unread_notifications": Notification.objects.filter(recipient=user, is_read=False).count(),
        }

        return Response(data, status=status.HTTP_200_OK)

# Generic CRUD base class for reuse
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
            obj = self.model_class.objects.all()
            serializer = self.serializer_class(obj, many=True)
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

# Individual views for each model
class RoleAPIView(BaseAPIView):
    model_class = Role
    serializer_class = RoleSerializer

class UserAPIView(BaseAPIView):
    model_class = User
    serializer_class = UserSerializer

class AgentProfileAPIView(BaseAPIView):
    model_class = AgentProfile
    serializer_class = AgentProfileSerializer

class BuyerProfileAPIView(BaseAPIView):
    model_class = BuyerProfile
    serializer_class = BuyerProfileSerializer

class TenantProfileAPIView(BaseAPIView):
    model_class = TenantProfile
    serializer_class = TenantProfileSerializer

class SellerProfileAPIView(BaseAPIView):
    model_class = SellerProfile
    serializer_class = SellerProfileSerializer

class PropertyTypeAPIView(BaseAPIView):
    model_class = PropertyType
    serializer_class = PropertyTypeSerializer

class LocationAPIView(BaseAPIView):
    model_class = Location
    serializer_class = LocationSerializer

class AmenityAPIView(BaseAPIView):
    model_class = Amenity
    serializer_class = AmenitySerializer

class PropertyAPIView(BaseAPIView):
    model_class = Property
    serializer_class = PropertySerializer

class PropertyImageAPIView(BaseAPIView):
    model_class = PropertyImage
    serializer_class = PropertyImageSerializer


# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
# from .models import *
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth import authenticate, login, logout
# from .forms import RegisterForm, LoginForm

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             role = Role.objects.get_or_create(name='buyer')[0]
#             user.roles.add(role)
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = RegisterForm()
#     return render(request, 'core/register.html', {'form': form})

# def login_view(request):
#     form = LoginForm(request, data=request.POST or None)
#     if form.is_valid():
#         user = form.get_user()
#         login(request, user)
#         return redirect('dashboard')
#     return render(request, 'core/login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')


# # View Seller Profile
# @login_required
# def seller_profile(request):
#     try:
#         seller = request.user.seller_profile
#         properties = seller.properties_for_sale.all()
#         return JsonResponse({
#             "seller": request.user.username,
#             "phone": seller.phone,
#             "properties": [prop.title for prop in properties]
#         })
#     except SellerProfile.DoesNotExist:
#         return HttpResponseForbidden("User is not a seller.")

# # Seller: List All Their Properties
# @login_required
# def seller_properties(request):
#     try:
#         seller = request.user.seller_profile
#         properties = seller.properties_for_sale.all()
#         return JsonResponse({
#             "properties": [
#                 {
#                     "id": prop.id,
#                     "title": prop.title,
#                     "price": float(prop.price),
#                     "status": prop.status
#                 } for prop in properties
#             ]
#         })
#     except SellerProfile.DoesNotExist:
#         return HttpResponseForbidden("User is not a seller.")

# # Seller: Add Property to Sale List (associate existing property to seller)
# @login_required
# @require_http_methods(["POST"])
# def add_property_to_sale(request, property_id):
#     try:
#         seller = request.user.seller_profile
#         property_obj = get_object_or_404(Property, id=property_id)

#         # Optional: Ensure this seller owns the property or it's not already linked
#         seller.properties_for_sale.add(property_obj)
#         return JsonResponse({"message": f"Property '{property_obj.title}' added to your sale list."})
#     except SellerProfile.DoesNotExist:
#         return HttpResponseForbidden("User is not a seller.")


# # USER DASHBOARD
# @login_required
# def dashboard(request):
#     return HttpResponse(f"Welcome {request.user.username}! You have roles: {[role.name for role in request.user.roles.all()]}")

# # PROPERTY LISTING
# @login_required
# def property_list(request):
#     properties = Property.objects.filter(status='available')
#     return JsonResponse({"properties": [prop.title for prop in properties]})

# # SINGLE PROPERTY DETAIL
# @login_required
# def property_detail(request, pk):
#     prop = get_object_or_404(Property, pk=pk)
#     return JsonResponse({
#         "title": prop.title,
#         "price": float(prop.price),
#         "location": str(prop.location),
#         "agent": prop.agent.username
#     })

# # PROPERTY POSTING (AGENT ONLY)
# @login_required
# @permission_required('core.add_property', raise_exception=True)
# def create_property(request):
#     if request.method == 'POST':
#         # Dummy implementation for frontend work
#         return HttpResponse("Property created (placeholder)")
#     return HttpResponse("Only POST allowed for creating properties")

# # PROFILE VIEWS
# @login_required
# def agent_profile(request):
#     try:
#         agent = request.user.agent_profile
#         return JsonResponse({"agent_id": agent.agent_id})
#     except:
#         return HttpResponse("No agent profile", status=404)

# @login_required
# def buyer_profile(request):
#     try:
#         buyer = request.user.buyer_profile
#         return JsonResponse({"buyer_id": buyer.buyer_id, "budget_min": float(buyer.budget_range_min or 0)})
#     except:
#         return HttpResponse("No buyer profile", status=404)

# @login_required
# def tenant_profile(request):
#     try:
#         tenant = request.user.tenant_profile
#         return JsonResponse({"preferred_city": tenant.preferred_city})
#     except:
#         return HttpResponse("No tenant profile", status=404)

# # FEATURED PROPERTIES
# def featured_properties(request):
#     featured = Property.objects.filter(is_featured=True)
#     return JsonResponse({"featured": [p.title for p in featured]})

# # LIST AMENITIES
# def list_amenities(request):
#     amenities = Amenity.objects.all()
#     return JsonResponse({"amenities": [a.name for a in amenities]})
