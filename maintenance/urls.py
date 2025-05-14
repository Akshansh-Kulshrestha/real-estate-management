
from django.urls import path
from .views import ServiceProviderAPIView, MaintenanceRequestAPIView, MaintenanceLogAPIView

urlpatterns = [
    path('service-providers/', ServiceProviderAPIView.as_view()),
    path('service-providers/<int:pk>/', ServiceProviderAPIView.as_view()),

    path('maintenance-requests/', MaintenanceRequestAPIView.as_view()),
    path('maintenance-requests/<int:pk>/', MaintenanceRequestAPIView.as_view()),

    path('maintenance-logs/', MaintenanceLogAPIView.as_view()),
    path('maintenance-logs/<int:pk>/', MaintenanceLogAPIView.as_view()),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('service-providers/', views.service_provider_list, name='service_provider_list'),
#     path('maintenance-requests/', views.maintenance_request_list, name='maintenance_request_list'),
#     path('maintenance-requests/<int:request_id>/', views.maintenance_request_detail, name='maintenance_request_detail'),
#     path('maintenance-requests/create/', views.create_maintenance_request, name='create_maintenance_request'),
#     path('maintenance-requests/<int:request_id>/add-log/', views.add_maintenance_log, name='add_maintenance_log'),
# ]
