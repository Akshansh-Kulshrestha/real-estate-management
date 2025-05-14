from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost, Notification, Message
from .serializers import BlogPostSerializer, NotificationSerializer, MessageSerializer


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
            queryset = self.model_class.objects.all()
            serializer = self.serializer_class(queryset, many=True)
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


class BlogPostAPIView(BaseAPIView):
    model_class = BlogPost
    serializer_class = BlogPostSerializer


class NotificationAPIView(BaseAPIView):
    model_class = Notification
    serializer_class = NotificationSerializer


class MessageAPIView(BaseAPIView):
    model_class = Message
    serializer_class = MessageSerializer

# from django.conf import settings
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from .models import BlogPost, Notification, Message
# from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone

# @login_required
# def published_blogposts(request):
#     posts = BlogPost.objects.filter(is_published=True)
#     return HttpResponse(f"{posts.count()} published blog post(s).")

# @login_required
# def unread_notifications(request):
#     notifications = Notification.objects.filter(recipient=request.user, is_read=False)
#     return HttpResponse(f"You have {notifications.count()} unread notification(s).")

# @login_required
# def inbox(request):
#     messages = Message.objects.filter(recipient=request.user)
#     return HttpResponse(f"You have {messages.count()} message(s) in your inbox.")

# @csrf_exempt
# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         recipient_id = request.POST.get('recipient_id')
#         content = request.POST.get('content')

#         if not content or not recipient_id:
#             return HttpResponse("Missing 'recipient_id' or 'content'", status=400)

#         try:
#             recipient = settings.AUTH_USER_MODEL.objects.get(id=recipient_id)
#         except Exception:
#             return HttpResponse("Recipient not found.", status=404)

#         Message.objects.create(
#             sender=request.user,
#             recipient=recipient,
#             content=content,
#             timestamp=timezone.now()
#         )

#         return HttpResponse(f"Message sent to {recipient.username}.")

#     return HttpResponse("Use POST to send a message.")
