# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
#     path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),

#     path('register/', RegisterAPIView.as_view(), name='register'),
#     path('login/', LoginAPIView.as_view(), name='login'),
#     path('logout/', LogoutAPIView.as_view(), name='logout'),

#     path('dashboard/', DashboardView.as_view(), name='dashboard'),

#     path('roles/', RoleAPIView.as_view()),
#     path('roles/<int:pk>/', RoleAPIView.as_view()),

#     path('users/', UserAPIView.as_view()),
#     path('users/<int:pk>/', UserAPIView.as_view()),

#     path('agents/', AgentProfileAPIView.as_view()),
#     path('agents/<int:pk>/', AgentProfileAPIView.as_view()),

#     path('buyers/', BuyerProfileAPIView.as_view()),
#     path('buyers/<int:pk>/', BuyerProfileAPIView.as_view()),

#     path('tenants/', TenantProfileAPIView.as_view()),
#     path('tenants/<int:pk>/', TenantProfileAPIView.as_view()),

#     path('sellers/', SellerProfileAPIView.as_view()),
#     path('sellers/<int:pk>/', SellerProfileAPIView.as_view()),

#     path('property-types/', PropertyTypeAPIView.as_view()),
#     path('property-types/<int:pk>/', PropertyTypeAPIView.as_view()),

#     path('locations/', LocationAPIView.as_view()),
#     path('locations/<int:pk>/', LocationAPIView.as_view()),

#     path('amenities/', AmenityAPIView.as_view()),
#     path('amenities/<int:pk>/', AmenityAPIView.as_view()),

#     path('properties/', PropertyAPIView.as_view()),
#     path('properties/<int:pk>/', PropertyAPIView.as_view()),

#     path('property-images/', PropertyImageAPIView.as_view()),
#     path('property-images/<int:pk>/', PropertyImageAPIView.as_view()),
# ]



from django.urls import path
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', views. register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('remove-profile-picture/', views.remove_profile_picture, name='remove_profile_picture'),

    path('', views.dashboard, name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('agents/add/', views.add_agent, name='add_agent'),
    path('agents/edit/<int:user_id>/', views.edit_agent, name='edit_agent'),  # correct
    path('agents/delete/<int:user_id>/', views.delete_agent, name='delete_agent'),

    path('admin/properties/add/', views.add_property, name='add_property'),
    path('admin/properties/edit/<int:pk>/', views.edit_property, name='edit_property'),
    path('admin/properties/delete/<int:pk>/', views.delete_property, name='delete_property'),
    path('admin/properties/approve/<int:pk>/', views.approve_property, name='approve_property'),


    path('properties/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/location/', views.location_view, name='location_view'),
    path('add/nearby', views.add_nearby, name='nearby-add'),
    path('ajax/get-cities/', views.get_cities, name='get_cities'),
    path('ajax/get-areas/', views.get_areas, name='get_areas'),
    path('ajax/get-pincodes/', views.get_pincodes, name='get_pincodes'),


    path('profile/agent/', views.agent_profile, name='agent_profile'),
    path('profile/buyer/', views.buyer_profile, name='buyer_profile'),
    path('profile/tenant/', views.tenant_profile, name='tenant_profile'),

    path('properties/featured/', views.featured_properties, name='featured_properties'),
    path('amenities/', views.list_amenities, name='list_amenities'),
    path('profile/seller/', views.seller_profile, name='seller_profile'),
    path('seller/properties/', views.seller_properties, name='seller_properties'),
    path('seller/property/add/<int:property_id>/', views.add_property_to_sale, name='add_property_to_sale'),
]
