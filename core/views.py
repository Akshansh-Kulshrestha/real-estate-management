# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import *
# from booking.models import *
# from blog.models import *
# from rest_framework.permissions import IsAuthenticated
# from .serializers import *
# from django.contrib.auth import logout
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User  
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.core.mail import send_mail
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.urls import reverse
# from rest_framework_simplejwt.settings import api_settings
# from datetime import timedelta
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode

# User = get_user_model()

# class CustomPasswordResetConfirmView(APIView):
#     def post(self, request, uidb64, token):
#         try:
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User.objects.get(pk=uid)

#             if not default_token_generator.check_token(user, token):
#                 return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

#             new_password = request.data.get('new_password')
#             confirm_password = request.data.get('confirm_password')

#             if new_password != confirm_password:
#                 return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

#             user.set_password(new_password)
#             user.save()

#             return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

#         except (User.DoesNotExist, ValueError, TypeError, OverflowError):
#             return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
# class ForgotPasswordAPIView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         try:
#             user = User.objects.filter(email=email).first()
#             if not user:
#                 return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#             token_generator = PasswordResetTokenGenerator()
#             token = token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))

#             reset_link = request.build_absolute_uri(
#                 reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
#             )

#             send_mail(
#                 subject='Reset your password',
#                 message=f'Click the link to reset your password: {reset_link}',
#                 from_email='noreply@yourapp.com',
#                 recipient_list=[user.email],
#             )

#             return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({
#                 'message': 'User registered successfully.',
#                 'user_id': user.id,
#                 'username': user.username
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class LoginAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         remember_me = request.data.get('remember_me', False)

#         user = authenticate(request, username=username, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)

#             if remember_me:
#                 # Extend the access/refresh token lifetime
#                 refresh.set_exp(lifetime=timedelta(days=30))
#                 refresh.access_token.set_exp(lifetime=timedelta(days=1))

#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user_id': user.id,
#                 'username': user.username,
#             })
#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class LogoutAPIView(APIView):
#     def post(self, request):
#         if request.user.is_authenticated:
#             request.user.auth_token.delete()
#             logout(request)
#             return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
#         return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         user_roles = list(user.roles.values_list("name", flat=True)) if hasattr(user, "roles") else []

#         try:
#             total_properties = Property.objects.filter(created_by=user).count()
#         except Exception:
#             total_properties = 0

#         try:
#             total_bookings = Booking.objects.filter(buyer__user=user).count()
#             pending_bookings = Booking.objects.filter(buyer__user=user, status='scheduled').count()
#         except Exception:
#             total_bookings = 0
#             pending_bookings = 0

#         try:
#             total_transactions = Transaction.objects.filter(buyer__user=user).count()
#         except Exception:
#             total_transactions = 0

#         try:
#             unread_messages = Message.objects.filter(recipient=user, is_read=False).count()
#         except Exception:
#             unread_messages = 0

#         try:
#             unread_notifications = Notification.objects.filter(recipient=user, is_read=False).count()
#         except Exception:
#             unread_notifications = 0

#         data = {
#             "username": user.username,
#             "email": user.email,
#             "role": user_roles,
#             "total_properties": total_properties,
#             "total_bookings": total_bookings,
#             "pending_bookings": pending_bookings,
#             "total_transactions": total_transactions,
#             "unread_messages": unread_messages,
#             "unread_notifications": unread_notifications,
#         }

#         return Response(data, status=status.HTTP_200_OK)


# # Generic CRUD base class for reuse
# class BaseAPIView(APIView):
#     model_class = None
#     serializer_class = None
#     permission_classes = [IsAuthenticated]  # Secure all views by default

#     def get_queryset(self, request):
#         # Default to returning all objects (can be overridden)
#         return self.model_class.objects.all()

#     def get_object(self, pk, request):
#         try:
#             return self.get_queryset(request).get(pk=pk)
#         except self.model_class.DoesNotExist:
#             return None

#     def get(self, request, pk=None):
#         if pk:
#             obj = self.get_object(pk, request)
#             if not obj:
#                 return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
#             serializer = self.serializer_class(obj)
#         else:
#             queryset = self.get_queryset(request)
#             serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)  # For models with `created_by`
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         obj = self.get_object(pk, request)
#         if not obj:
#             return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = self.serializer_class(obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         obj = self.get_object(pk, request)
#         if not obj:
#             return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
#         obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # Individual views for each model
# class RoleAPIView(BaseAPIView):
#     model_class = Role
#     serializer_class = RoleSerializer
#     def get_queryset(self, request):
#         return Role.objects.filter(created_by=request.user)
# class UserAPIView(BaseAPIView):
#     model_class = User
#     serializer_class = UserSerializer
#     def get_queryset(self, request):
#         return User.objects.filter(created_by=request.user)

# class AgentProfileAPIView(BaseAPIView):
#     model_class = AgentProfile
#     serializer_class = AgentProfileSerializer

#     def get_queryset(self, request):
#         if request.user.is_authenticated:
#             request.user.add_role('Agent')  # ✅ assign role and auto-create profile
#             return AgentProfile.objects.filter(user=request.user)
#         return AgentProfile.objects.none()


# class BuyerProfileAPIView(BaseAPIView):
#     model_class = BuyerProfile
#     serializer_class = BuyerProfileSerializer
#     def get_queryset(self, request):
#         return BuyerProfile.objects.filter(user=request.user)

# class TenantProfileAPIView(BaseAPIView):
#     model_class = TenantProfile
#     serializer_class = TenantProfileSerializer
#     def get_queryset(self, request):
#         return TenantProfile.objects.filter(user=request.user)

# class SellerProfileAPIView(BaseAPIView):
#     model_class = SellerProfile
#     serializer_class = SellerProfileSerializer
#     def get_queryset(self, request):
#         return SellerProfile.objects.filter(user=request.user)

# class PropertyTypeAPIView(BaseAPIView):
#     model_class = PropertyType
#     serializer_class = PropertyTypeSerializer
#     def get_queryset(self, request):
#             return PropertyType.objects.all()

# class LocationAPIView(BaseAPIView):
#     model_class = Location
#     serializer_class = LocationSerializer
#     def get_queryset(self, request):
#             return Location.objects.all()

# class AmenityAPIView(BaseAPIView):
#     model_class = Amenity
#     serializer_class = AmenitySerializer
#     def get_queryset(self, request):
#             return Amenity.objects.all()

# class PropertyAPIView(BaseAPIView):
#     model_class = Property
#     serializer_class = PropertySerializer
#     def get_queryset(self, request):
#             return Property.objects.all()
# class PropertyImageAPIView(BaseAPIView):
#     model_class = PropertyImage
#     serializer_class = PropertyImageSerializer
#     def get_queryset(self, request):
#         return PropertyImage.objects.all()

#---------------------------------------------------------------------------------------#

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'auth/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "User with this email does not exist.")
            return render(request, 'auth/forgot_password.html')

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            subject='Reset your password',
            message=f'Click the link to reset your password: {reset_link}',
            from_email='noreply@yourapp.com',
            recipient_list=[user.email],
        )

        messages.success(request, 'Password reset link sent to your email.')
        return redirect('forgot-password')


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        return render(request, 'auth/reset_password.html', {'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                messages.error(request, "Invalid or expired token.")
                return redirect('forgot-password')

            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'auth/reset_password.html', {'uidb64': uidb64, 'token': token})

            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. You can now log in.")
            return redirect('login')

        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            messages.error(request, "Invalid password reset request.")
            return redirect('forgot-password')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # role = Role.objects.get_or_create(name='buyer')[0]
            # user.roles.add(role)
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'core/login1.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# View Seller Profile
@login_required
def seller_profile(request):
    try:
        seller = request.user.seller_profile
        properties = seller.properties_for_sale.all()
        return JsonResponse({
            "seller": request.user.username,
            "phone": seller.phone,
            "properties": [prop.title for prop in properties]
        })
    except SellerProfile.DoesNotExist:
        return HttpResponseForbidden("User is not a seller.")

# Seller: List All Their Properties
@login_required
def seller_properties(request):
    try:
        seller = request.user.seller_profile
        properties = seller.properties_for_sale.all()
        return JsonResponse({
            "properties": [
                {
                    "id": prop.id,
                    "title": prop.title,
                    "price": float(prop.price),
                    "status": prop.status
                } for prop in properties
            ]
        })
    except SellerProfile.DoesNotExist:
        return HttpResponseForbidden("User is not a seller.")

# Seller: Add Property to Sale List (associate existing property to seller)
@login_required
@require_http_methods(["POST"])
def add_property_to_sale(request, property_id):
    try:
        seller = request.user.seller_profile
        property_obj = get_object_or_404(Property, id=property_id)

        # Optional: Ensure this seller owns the property or it's not already linked
        seller.properties_for_sale.add(property_obj)
        return JsonResponse({"message": f"Property '{property_obj.title}' added to your sale list."})
    except SellerProfile.DoesNotExist:
        return HttpResponseForbidden("User is not a seller.")


# USER DASHBOARD
@login_required
def dashboard(request):
    roles = request.user.roles.all()
    image = PropertyImage.objects.all()
    pro_name = Property.objects.all()
    return render(request, 'core/index.html', {'username': request.user.username, 'roles': roles, 'image' : image, 'pro_name': pro_name})

# PROPERTY LISTING
@login_required
def property_list(request):
    properties = Property.objects.filter(status='available')
    return JsonResponse({"properties": [prop.title for prop in properties]})

# SINGLE PROPERTY DETAIL
@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    return JsonResponse({
        "title": prop.title,
        "price": float(prop.price),
        "location": str(prop.location),
        "agent": prop.agent.username
    })

# PROPERTY POSTING (AGENT ONLY)
@login_required
@permission_required('core.add_property', raise_exception=True)
def create_property(request):
    if request.method == 'POST':
        # Dummy implementation for frontend work
        return HttpResponse("Property created (placeholder)")
    return HttpResponse("Only POST allowed for creating properties")

# PROFILE VIEWS
@login_required
def agent_profile(request):
    
    try:
        agent = AgentProfile.objects.all().values()
        return JsonResponse({"agent": list(agent)})
    except:
        return HttpResponse("No agent profile", status=404)

@login_required
def buyer_profile(request):
    try:
        buyer = request.user.buyer_profile
        return JsonResponse({"buyer_id": buyer.buyer_id, "budget_min": float(buyer.budget_range_min or 0)})
    except:
        return HttpResponse("No buyer profile", status=404)

@login_required
def tenant_profile(request):
    try:
        tenant = request.user.tenant_profile
        return JsonResponse({"preferred_city": tenant.preferred_city})
    except:
        return HttpResponse("No tenant profile", status=404)

# FEATURED PROPERTIES
def featured_properties(request):
    featured = Property.objects.filter(is_featured=True)
    return JsonResponse({"featured": [p.title for p in featured]})

# LIST AMENITIES
def list_amenities(request):
    amenities = Amenity.objects.all()
    return JsonResponse({"amenities": [a.name for a in amenities]})
