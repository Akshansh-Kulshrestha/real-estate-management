from django.urls import path
from .views import *

urlpatterns = [
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('roles/', RoleAPIView.as_view()),
    path('roles/<int:pk>/', RoleAPIView.as_view()),

    path('users/', UserAPIView.as_view()),
    path('users/<int:pk>/', UserAPIView.as_view()),

    path('agents/', AgentProfileAPIView.as_view()),
    path('agents/<int:pk>/', AgentProfileAPIView.as_view()),

    path('buyers/', BuyerProfileAPIView.as_view()),
    path('buyers/<int:pk>/', BuyerProfileAPIView.as_view()),

    path('tenants/', TenantProfileAPIView.as_view()),
    path('tenants/<int:pk>/', TenantProfileAPIView.as_view()),

    path('sellers/', SellerProfileAPIView.as_view()),
    path('sellers/<int:pk>/', SellerProfileAPIView.as_view()),

    path('property-types/', PropertyTypeAPIView.as_view()),
    path('property-types/<int:pk>/', PropertyTypeAPIView.as_view()),

    path('locations/', LocationAPIView.as_view()),
    path('locations/<int:pk>/', LocationAPIView.as_view()),

    path('amenities/', AmenityAPIView.as_view()),
    path('amenities/<int:pk>/', AmenityAPIView.as_view()),

    path('properties/', PropertyAPIView.as_view()),
    path('properties/<int:pk>/', PropertyAPIView.as_view()),

    path('property-images/', PropertyImageAPIView.as_view()),
    path('property-images/<int:pk>/', PropertyImageAPIView.as_view()),
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register/', views. register_view, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),

#     path('', views.dashboard, name='dashboard'),
#     path('properties/', views.property_list, name='property_list'),
#     path('property/<int:pk>/', views.property_detail, name='property_detail'),
#     path('property/create/', views.create_property, name='create_property'),

#     path('profile/agent/', views.agent_profile, name='agent_profile'),
#     path('profile/buyer/', views.buyer_profile, name='buyer_profile'),
#     path('profile/tenant/', views.tenant_profile, name='tenant_profile'),

#     path('properties/featured/', views.featured_properties, name='featured_properties'),
#     path('amenities/', views.list_amenities, name='list_amenities'),
#     path('profile/seller/', views.seller_profile, name='seller_profile'),
#     path('seller/properties/', views.seller_properties, name='seller_properties'),
#     path('seller/property/add/<int:property_id>/', views.add_property_to_sale, name='add_property_to_sale'),
# ]
