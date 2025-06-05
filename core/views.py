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
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from .models import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User

User = get_user_model()



class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = CustomPasswordResetForm
    success_url = '/home/password_reset/done/'

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
        else:
            print(form.errors)  # or log this properly
            messages.error(request, 'There was an error in your form. Please correct it.')
    else:
        initial_data= {'username': '',
                        'email': '',
                          'password1': '',
                            'password2':'',
                              'first_name' : '', 
                              'last_name' : '',
                              'phone':'',
                              'state':'',
                              'city':''
                              }
        form = RegisterForm(initial=initial_data)
        
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(6000)  # Session expires after ~100 minutes

            # Redirect based on user type
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')  # Define your regular user dashboard URL name
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

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
def dashboard(request):
    property = Property.objects.all()
    return render(request, 'core/landing-page.html', {'username': request.user.username, 'property' : property})


def is_admin(user):
    return user.is_superuser or user.roles.filter(name="superadmin").exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    user=request.user
    today = timezone.now().date()
   
    seven_days_ago = today - timedelta(days=7)

    new_today = Property.objects.filter(date_posted__date=today).count()
    new_last_7_days = Property.objects.filter(date_posted__date__gte=seven_days_ago).count()
    latest_properties = Property.objects.all()  # Sorted by min to max
    today = now().date()
    agent = UserRole.objects.filter(role__name='Agent')
    agent_user_ids = AgentProfile.objects.values_list('user_id', flat=True)
    total_users = User.objects.exclude(is_superuser=True).exclude(id__in=agent_user_ids).count()
    width_total_users = total_users * 10
    total_properties= Property.objects.count()
    width_total_properties= total_properties * 10
    total_agents = User.objects.filter(roles__name='Agent').distinct().count()
    width_total_agents = total_agents * 10
    total_properties_sold = Property.objects.filter(status='sold').count()
    width_total_properties_sold = total_properties_sold * 10

    

    context = {
        'agent': agent ,
        'profile' : User.objects.filter(id=user.id),
        'total_users': total_users, 
        'width_total_users': width_total_users,
        'total_properties': total_properties,
        'width_total_properties': width_total_properties,
        'total_agents': total_agents,
        'width_total_agents': width_total_agents,
        'total_properties_sold' : total_properties_sold,
        'width_total_properties_sold' : width_total_properties_sold,
        'current': timezone.now(),
        'today': today,
        'new_today': new_today,
        'new_last_7_days': new_last_7_days,
        'latest_properties': latest_properties,
        
    }
    
    return render(request, 'core/admin_dashboard.html', context)

def is_admin(user):
    return user.is_superuser
#-----------Agent Actions----------------#

@login_required
@user_passes_test(is_admin)
def add_agent(request):
    existing_agents = User.objects.filter(roles__name='Agent')

    if request.method == 'POST':
        form = AgentForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the new user

            # Assign the 'Agent' role
            agent_role = get_object_or_404(Role, name='Agent')
            UserRole.objects.get_or_create(user=user, role=agent_role)

            # No need to manually trigger the signal – it will run automatically
            return redirect('admin_dashboard')
    else:
        form = AgentForm()

    return render(request, 'core/agents/add_agent.html', {'form': form, 'agent': existing_agents})


@login_required
@user_passes_test(is_admin)
def edit_agent(request, user_id):
    user = get_object_or_404(User, id=user_id)
    agent = UserRole.objects.filter(role__name='Agent')

    form = AgentForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'core/agents/edit_agent.html', {'form': form, 'agent':agent})

@login_required
@user_passes_test(is_admin)
def delete_agent(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

#-----------Property Actions----------------#
def is_admin_or_seller_or_agent(user):
    return user.is_superuser or user.has_role('Seller') or user.has_role('Agent')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            property_instance = form.save(commit=False)

            if request.user.is_superuser:
                # Admin must explicitly assign an owner
                if not property_instance.owner:
                    return HttpResponseBadRequest("Admin must select an owner.")
            else:
                # For non-admins, assign current user as owner and user
                property_instance.owner = request.user
                property_instance.user = request.user

            property_instance.save()
            form.save_m2m()

            # Save uploaded images from input named 'images'
            for img in request.FILES.getlist('images'):
                PropertyImage.objects.create(property=property_instance, image=img)

            messages.success(request, "Property added successfully.")
            return redirect('property_list')
    else:
        form = PropertyForm(user=request.user)

    return render(request, 'core/properties/add_property.html', {'form': form})


@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    # Permissions: only owner or superuser can edit
    if not request.user.is_superuser and property_obj.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this property.")

    if request.method == 'POST':
        # Delete selected images (IDs come from 'delete_images' checkboxes)
        images_to_delete = request.POST.getlist('delete_images')
        PropertyImage.objects.filter(id__in=images_to_delete, property=property_obj).delete()

        form = PropertyForm(request.POST, request.FILES, instance=property_obj, user=request.user)
        if form.is_valid():
            property_instance = form.save(commit=False)

            if not request.user.is_superuser:
                # Prevent non-admins from changing owner or user fields
                property_instance.owner = request.user
                property_instance.user = request.user

            property_instance.save()
            form.save_m2m()

            # Save newly uploaded images
            for img in request.FILES.getlist('images'):
                PropertyImage.objects.create(property=property_instance, image=img)

            messages.success(request, 'Property updated successfully.')
            return redirect('edit_property', pk=property_instance.pk)
    else:
        form = PropertyForm(instance=property_obj, user=request.user)

    property_images = property_obj.images.all()

    return render(request, 'core/properties/edit_property.html', {
        'form': form,
        'property': property_obj,
        'images': property_images,
    })





@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def approve_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.is_featured = True
    property.save()
    messages.success(request, 'Property approved.')
    return redirect('admin_dashboard')




# PROPERTY LISTING
@login_required
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'core/properties/property_list.html', {'properties': properties})




@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if request.user.is_superuser or request.user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        print(form)
        # Don't reassign form here — just fall through to rendering with the same form
    else:
        form = UserForm(instance=user)

    return render(request, 'core/edit-profile.html', {'form': form})

@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and 'image' in request.FILES:
        user = request.user
        user.image = request.FILES['image']
        user.save()
    return redirect('edit_profile')

@login_required
def remove_profile_picture(request):
    user = request.user
    user.image.delete(save=True)  # Deletes the image file too
    return redirect('edit_profile')

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

def property_gallery_view(request, property_id):
    property = Property.objects.get(id=property_id)
    images = property.images.all()  # ✅ this gets ALL images for this property

    return render(request, 'your_template.html', {
        'image': images,        # ← this must be a QuerySet, not a single image
        'pro_name': [property]  # ← since your template expects a list here
    })


def location_view(request):
    location = Location.objects.all()
    return JsonResponse({"location": [a.name for a in location]})   
        
def get_cities(request):
    state = request.GET.get('state')
    cities = Location.objects.filter(state=state).values_list('city', flat=True).distinct()
    return JsonResponse({'cities': list(cities)})

def get_areas(request):
    state = request.GET.get('state')
    city = request.GET.get('city')
    areas = Location.objects.filter(state=state, city=city).values_list('area', flat=True).distinct()
    return JsonResponse({'areas': list(areas)})

def get_pincodes(request):
    state = request.GET.get('state')
    city = request.GET.get('city')
    area = request.GET.get('area')
    pincodes = Location.objects.filter(state=state, city=city, area=area).values_list('pincode', flat=True).distinct()
    return JsonResponse({'pincodes': list(pincodes)})


def add_nearby(request):
    if request.method == 'POST':
        form = NearbyForm(request.POST)
        if form.is_valid():
            nearby = form.save(commit=False)
            property_id = request.POST.get('property_id')
            from .models import Property  # adjust if needed
            nearby.property = Property.objects.get(id=property_id)
            nearby.save()
            return JsonResponse({'success': True, 'id': nearby.id, 'name': nearby.name})
        return JsonResponse({'success': False, 'errors': form.errors})

    property_id = request.GET.get('property_id')  # passed via ?property_id=123 in URL
    form = NearbyForm()
    return render(request, 'core/properties/nearby.html', {'form': form, 'property_id': property_id})

# SINGLE PROPERTY DETAIL
def property_detail(request, pk):
    properties = Property.objects.all()
    return render(request, 'home/property_detail.html', {'property': properties})