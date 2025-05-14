from django.urls import path
from .views import (
    PropertyViewListCreateAPIView,
    SearchQueryListCreateAPIView,
    FeedbackListCreateAPIView,
)

urlpatterns = [
    path('property-views/', PropertyViewListCreateAPIView.as_view(), name='property-views'),
    path('search-queries/', SearchQueryListCreateAPIView.as_view(), name='search-queries'),
    path('feedback/', FeedbackListCreateAPIView.as_view(), name='feedback'),
]

# from django.shortcuts import render
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('views/', views.property_view_list, name='property_views'),
#     path('queries/', views.search_query_list, name='search_queries'),
#     path('feedback/', views.feedback_create, name='submit_feedback'),
#     path('feedback/thank-you/', lambda request: render(request, 'feedback_thankyou.html'), name='feedback_thankyou'),
# ]
