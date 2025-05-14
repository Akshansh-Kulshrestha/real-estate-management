from django.urls import path
from .views import BlogPostAPIView, NotificationAPIView, MessageAPIView

urlpatterns = [
    path('blog-posts/', BlogPostAPIView.as_view()),
    path('blog-posts/<int:pk>/', BlogPostAPIView.as_view()),
    
    path('notifications/', NotificationAPIView.as_view()),
    path('notifications/<int:pk>/', NotificationAPIView.as_view()),
    
    path('messages/', MessageAPIView.as_view()),
    path('messages/<int:pk>/', MessageAPIView.as_view()),
]


# # content/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('blogposts/', views.published_blogposts, name='published_blogposts'),
#     path('notifications/unread/', views.unread_notifications, name='unread_notifications'),
#     path('messages/inbox/', views.inbox, name='inbox'),
#     path('messages/send/', views.send_message, name='send_message'),
# ]
